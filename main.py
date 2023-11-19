from bcrypt import hashpw, checkpw, gensalt
import click
import os
from db import get_db
import mysql
import logging

logger = logging.getLogger("mylog")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# open connectino to database
conn = get_db()

logger.info("Initiated application")

ADMIN = 1
REGULAR = 0
FAILURE = -1
EXIT = -2
SUCCESS = 0


def create_admin():
    """Create admin.

    NOTE: Only root user can create admin.

    First create a new member, then move the member into admin position.
    """
    logger.info("Getting root password from user")
    # Check root status
    root_pw = click.prompt("Enter root password: ", hide_input=True)

    logger.info("Getting root password from environment variables.")
    if root_pw != os.getenv("ROOT"):
        logger.error("Password authentication failed")
        click.echo("You're not root. Good luck next time!")
        return FAILURE

    try:
        # create as regular member first
        logger.info("Creating new member")

        username = create_member()
        
        if username == FAILURE:
            click.echo("Fail to create new member.")
            logger.info("Fail to create new member.")
            return FAILURE
        
        cursor = conn.cursor()

        insert_admin = f"INSERT INTO admin VALUES ('{username}')"

        # Execute the query
        logger.info("Move member to admin role.")
        cursor.execute(insert_admin)
        conn.commit()

        logger.info("Admin created")
        return ADMIN
    except mysql.connector.Error as err:
        click.echo(f"Execution halt: {err}")
        return FAILURE


def create_member() -> str:
    """Create a regular member.

    Prompt users for input then create according member.
    """
    # get user input
    logger.info("Getting user input")
    username = click.prompt("Enter your username: ", str)

    click.echo("Are you an exlclusive member? [y]=exclusive, [n]=regular")
    c = click.getchar()
    if c == "y":
        membership_type = "exclusive"
    else:
        membership_type = "regular"
    
    password = click.prompt("Enter your password: ", str, hide_input=True)
    
    logger.info("Get cursor")
    cursor = conn.cursor()

    # first, hash the password for member before storing
    logger.info("Hash user password")
    hashed_pw = hashpw(bytes(password, 'utf-8'), gensalt())
    insert_member = "INSERT INTO member VALUES (%s, %s, %s, NOW())"
    member_data = (username, membership_type, hashed_pw)

    # execute and commit
    try:
        logger.info("Insert member into database")

        cursor.execute(insert_member, member_data)
        cursor.close()
        conn.commit()
    except mysql.connector.Error as err:
        logger.error(f"Failed to insert: {err}")
        click.echo(f"Execution halt: {err}")
        return FAILURE
    
    logger.info("Member created.")
    return username


def login() -> int:
    """Log the user into the system.

    Returns:
        A flag corresponding to the status of the authentication.
        1 for admin users.
        0 for regular user.
        -1 for failed login.
    """
    logger.info("Login. Getting user input")
    username = click.prompt("Enter your username: ", str)
    password = click.prompt("Enter your password: ", str, hide_input=True)
    
    # Username for this session of the application.
    global USERNAME

    try:
        cursor = conn.cursor()
        # Get all member password and username
        get_admins = "SELECT username FROM admin"
        
        logger.info("Get all admin names")
        cursor.execute(get_admins)

        names = cursor.fetchall()
        admin_names = set([name[0] for name in names])
        get_members = "SELECT username, pw FROM member"
        
        logger.info("Get all members username and password")
        cursor.execute(get_members)

        combs = cursor.fetchall()

        logger.info(f"Searching correct pw/username combination for {username}")
        for stored_username, stored_pw in combs:
            if (username == stored_username) and checkpw(bytes(password, 'utf-8'), bytes(stored_pw)):
                logger.info("Authenticates successfully. \
                            Checking if member is an admin.")
                if username in admin_names:
                    logger.info(f"{username} is an admin")
                    logger.info("Admin logged in.")

                    USERNAME = username
                    cursor.close()
                    return ADMIN
                
                cursor.close()
                logger.info(f"{username} is a regular member.")
                logger.info("Regular user logged in.")

                USERNAME = username
                return REGULAR
        
        click.echo("Wrong pw/username combination.")
        logger.error("Pw/Username doesn't exist. Execution halt.")
        cursor.close()
        return FAILURE
    except mysql.connector.Error as err:
        click.echo(f"Execution halt {err}")
        logger.error(f"Execution halt {err}")

        return FAILURE


def view_contest():
    logger.info("View contest.")
    query = "SELECT * FROM contest"

    logger.info("Get all contest in database.")
    cursor = conn.cursor()
    cursor.execute(query)
    contests = cursor.fetchall()

    if not contests:
        logger.error("Database doesn't have any contest.")
        logger.error("View contest - failure")
        click.echo("No contest found!")
        return FAILURE

    logger.info("Printing out contest information.")
    click.echo("Here's a list of contest.")
    for contest in contests:
        print(contest)

    logger.info("View contest - success")
    return SUCCESS


def host_contest():
    logger.info("host contest - ininiated")
    logger.info("Getting user input")
    contest_name = click.prompt("Enter contest name: ", str)
    capacity = click.prompt("Enter contest capacity: ", int)
    rules = click.prompt("Enter contest rules: ", str)
    rewards = click.prompt("Enter contest rewards: ", str)

    insert_contest = "INSERT INTO contest \
        (contest_name, capacity, requirements, date_created) \
        VALUES (%s, %s, %s, NOW())"
    contest_data = (contest_name, capacity, rules)

    try:
        cursor = conn.cursor()

        logger.info("Insert contest into database")
        cursor.execute(insert_contest, contest_data)

        logger.info("Get id of last inserted contest")
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        contest_host = "INSERT INTO contest_host VALUES (%s, %s, %s)"
        contest_host_data = (USERNAME, last_id, rewards)

        logger.info("Insert into contest_host the host information.")
        cursor.execute(contest_host, contest_host_data)

        cursor.close()
        conn.commit()
        logger.info("host contest - succeeded")

        return SUCCESS
    except mysql.connector.Error as err:
        click.echo(f"Execution halt {err}")
        logger.error(f"Execution halt: {err}")
        return FAILURE


def modify_contest():
    logger.info("Modify contest - initiated")
    # Figure out which contest to modify
    click.echo("Which contest are you trying to modify?")

    # Get all contest
    logger.info("Modify contest - get all contest.")
    if view_contest() == FAILURE:
        click.echo("No contests to modify")
        logger.error("No contest available to modify.")
        return FAILURE

    logger.info("Getting user input")
    edit_id = click.prompt("Enter id of contest you want to edit: ", int)
    contest_name = click.prompt("Enter contest name: ", str)
    capacity = click.prompt("Enter contest capacity: ", int)
    rules = click.prompt("Enter contest rules: ", str)

    edit_contest = "UPDATE contest SET \
        contest_name=%s, capacity=%s, requirements=%s\
        WHERE cid=%s"

    edit_data = (contest_name, capacity, rules, edit_id)
    try:
        cursor = conn.cursor()

        logger.info(f"Editing contest with cid={edit_id}")
        cursor.execute(edit_contest, edit_data)
        cursor.close()
        conn.commit()

        logger.info("Modify contest - succeeded")
        return SUCCESS
    except mysql.connector.Error as err:
        click.echo(f"Execution halt {err}")
        logger.info(f"Execution halt {err}")
        return FAILURE


def delete_contest():
    logger.info("Delete contest - initiated")

    logger.info("Delete contest - get all possible contest")
    if view_contest() == FAILURE:
        logger.error("No contest to delete")
        click.echo("No contest to delete.")
        logger.info("Delete contest - failed")
        return FAILURE
    
    logger.info("Getting user input")
    delete_id = click.prompt("Enter id of contest you want to edit: ", int)
    delete_query = f"DELETE FROM contest WHERE cid={delete_id}"
    try:
        logger.info(f"Delete contest with cid={delete_id}")
        cursor = conn.cursor()
        cursor.execute(delete_query)
        cursor.close()
        conn.commit()

        logger.info("Delete contest - succeeded")
        return SUCCESS
    except mysql.connector.Error as err:
        click.echo(f"Error. Execution halt: {err}")
        logger.info(f"Execution halt: {err}")
        logger.info("Delete contest - failed")
        return FAILURE
    

def admin_actions():
    prompt = '''
    Here's what you can do:
    [1] View all contests
    [2] Host a new contest
    [3] Modify a contest
    [4] Delete a contest
    [5] Exit
    '''

    click.echo(prompt)

    c = click.getchar()

    if c == '1':
        view_contest()
    elif c == '2':
        host_contest()
    elif c == '3':
        modify_contest()
    elif c == '4':
        delete_contest()
    else:
        return FAILURE


def regular_view():
    pass


def app():
    while True:
        prompts = '''
        What are you trying to do? \n\
        [1] Create an admin.
        [2] Login.
        [3] Exit.
        '''
        
        click.echo(prompts, nl=False)

        c = click.getchar()

        if c == '1':
            click.echo("Creating an admin.")
            create_admin()
        elif c == '2':
            click.echo("Logging you in.")
            status = login()

            if status == REGULAR:
                click.echo("You can do regular thing")
            elif status == ADMIN:
                click.echo("You can do admin thing")

                action_status = admin_actions()

                while action_status != FAILURE:
                    action_status = admin_actions()

                break
        elif c == '3':
            click.echo("Bye!")
            break
        else:
            return app()
    

# main application loop
if __name__ == "__main__":
    app()
    logger.info("Close database connection.")
    conn.close()
