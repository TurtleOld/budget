import os
import psycopg2 as psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()
dbname = os.getenv("dbname")
user = os.getenv("username").lower()
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")


# Подключение к базе данных

try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Подключение к базе произошло успешно!")

except (Exception, Error) as e:
    print(e)

connection.autocommit = True
cursor = connection.cursor()
