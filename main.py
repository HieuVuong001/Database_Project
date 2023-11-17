import click
from db import get_db
import bcrypt

# open connectino to database
conn = get_db()

def create_admin():
    """Create admin.

    First create a new member, then move the member into admin position.
    """
    # create as regular member first
    username = create_member()
    cursor = conn.cursor()

    insert_admin = f"INSERT INTO admin VALUES ('{username}')"

    # Execute the query
    cursor.execute(insert_admin)
    conn.commit()
    conn.close()

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
    
    password = click.prompt("Enter your password: ", str)
    
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


if __name__ == "__main__":
    try:
        prompts = '''What are you trying to do? \n\
            [1] Create an admin.
            [2] Login.
            '''
        
        click.echo(prompts, nl=False)

        c = click.getchar()

        if c == '1':
            click.echo("Creating an admin.")
            create_admin()
        else:
            click.echo("Coming soon!")
        # close the connection
        conn.close()
    except click.Abort:
        click.echo("\nUser exited.")
        exit
