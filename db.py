# SJSU CMPE 138 FALL 2023 TEAM3
import mysql.connector
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Give credentials to the connector
mydb = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERNAME'),
    password=os.getenv('PW'),
    database="keyboard_social"
)

def get_db():
    return mydb