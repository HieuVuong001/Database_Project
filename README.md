# Database_Project

Useful documentations:

[Click](https://click.palletsprojects.com/en/8.1.x/quickstart/)

[MySQLConnector](https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html)

[BCrypt](https://github.com/pyca/bcrypt/)


# Usage

1. Set up your virtual environment (optional).
2. Install the needed packages

```
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials (remember to match environment variables with the variables used in the python code). For example:

```
HOST="HOSTNAME"
USERNAME="John"
PW="123456"
```

4. Run `db.py`.

```
python3 db.py
```

To create the database:

1. In `mysql`, do:

```
source PATH_TO_FILE
```

where PATH_TO_FILE is the path to `create_database.sql`


To see how to use the main script:

```
python3 main.py --help
```