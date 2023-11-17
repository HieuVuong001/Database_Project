import click
from db import get_db
import bcrypt
from dotenv import load_dotenv
import os

# open connectino to database
conn = get_db()

ADMIN = 1
REGULAR = 0
FAILURE = -1
EXIT = -2

def create_admin():
    """Create admin.

    NOTE: Only root user can create admin.

    First create a new member, then move the member into admin position.
    """
    # Check root status
    root_pw = click.prompt("Enter root password: ", hide_input=True)

    if root_pw != os.getenv("ROOT"):
        click.echo("You're not root. Good luck next time!")
        return FAILURE

    # create as regular member first
    username = create_member()
    cursor = conn.cursor()

    insert_admin = f"INSERT INTO admin VALUES ('{username}')"

    # Execute the query
    cursor.execute(insert_admin)
    conn.commit()
    conn.close()

    return ADMIN

def create_member() -> str:
    """Create a regular member.

    Prompt users for input then create according member.
    """
    # get user input
    username = click.prompt("Enter your username: ", str)

    click.echo("Are you an exlclusive member? [y]=exclusive, [n]=regular")
    c = click.getchar()
    if c == "y":
        membership_type = "exclusive"
    else:
        membership_type = "regular"
    
    password = click.prompt("Enter your password: ", str, hide_input=True)
    
    cursor = conn.cursor()

    # first, hash the password for member before storing
    hashed_pw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    insert_member = f"INSERT INTO member VALUES (%s, %s, %s, NOW())"
    member_data = (username, membership_type, hashed_pw)

    # execute and commit
    cursor.execute(insert_member, member_data)
    cursor.close()
    conn.commit()

    return username

def login() -> int:
    """Log the user into the system.

    Returns:
        A flag corresponding to the status of the authentication.
        1 for admin users.
        0 for regular user.
        -1 for failed login.
    """
    username = click.prompt("Enter your username: ", str)
    password = click.prompt("Enter your password: ", str, hide_input=True)

    cursor = conn.cursor()

    # Get all member password and username
    get_members = f"SELECT username, pw FROM member"

    cursor.execute(get_members)

    for stored_username, stored_pw in cursor:
        if username == stored_username:
            if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(stored_pw)):
                # successfully login

                # determine if the current user is admin or regular member
                get_admins = f"SELECT username FROM admin"

                cursor.execute(get_admins)

                for stored_admin in cursor:
                    if username == stored_admin:
                        # found admin
                        click.echo(f"Welcome back, admin {username}")

                        return ADMIN

                click.echo(f"Welcome back, {username}")

                return REGULAR

    # cannot find member in the database
    click.echo("Wrong username or password. Try again.")

    return FAILURE

def admin_view():
    pass

def regular_view():
    pass

def app():
    try:
        while True:
            prompts = '''What are you trying to do? \n\
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

                
            elif c =='3':
                click.echo("Bye!")
                break
            else:
                return app()
    finally:
        conn.close()
    

# main application loop
if __name__ == "__main__":
    app()
        
