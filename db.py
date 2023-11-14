import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERNAME'),
    password=os.getenv('PW')
)


cursor = mydb.cursor()

cursor.execute("SHOW DATABASES")

for db_name in cursor:
    print(db_name)
