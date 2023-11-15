import click
from db import get_db
import bcrypt

# open connectino to database
conn = get_db()

@click.command()
@click.argument('username')
@click.argument('membership_type')
@click.argument('password')
def create_member(username, membership_type, password):
    # Create a cursor
    cursor = conn.cursor()

    # hash password
    # must cast string to bytes first
    hashed_pw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    # need username, membership_type, pw, and date_joined
    # NOW is a function of SQL to generate current date time
    query = f"INSERT INTO member VALUES (%s, %s, %s, NOW())"
    query_data = (username, membership_type, hashed_pw)
    
    # Execute the query
    cursor.execute(query, query_data)

    # Commit the change to the DB
    conn.commit()


if __name__ == "__main__":
    create_member()

    # close the connection
    conn.close()