import mysql.connector
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Give credentials to the connector
mydb = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERNAME'),
    password=os.getenv('PW')
)

# Create a cursor and execute sql statement
cursor = mydb.cursor()
cursor.execute("SHOW DATABASES")

# Print out result of the statement
for db_name in cursor:
    print(db_name)
