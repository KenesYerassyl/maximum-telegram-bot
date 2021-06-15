import psycopg2
from dotenv import load_dotenv
from os import environ
from psycopg2 import pool

load_dotenv()

class DBController:

    def __init__(self) -> None:
        self.pool = pool.ThreadedConnectionPool(
            1, 1,
            host = environ.get("DB_HOST"), 
            database = environ.get("DB_NAME"),
            user = environ.get("DB_NAME"),
            password = environ.get("DB_PASSWORD")
        )
    
    def does_chat_exist(self, chat_id):
        connection = self.pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM subscriptions WHERE chat_id=%s', (str(chat_id),))
            result = cursor.fetchall()
        connection.commit()
        self.pool.putconn(connection)
        return bool(len(result))

    def add_subscriber(self, chat_id, user_id, status = True):
        connection = self.pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO subscriptions (chat_id, user_id, status) VALUES (%s, %s, %s)', (str(chat_id), user_id, status))
        connection.commit()
        self.pool.putconn(connection)

    def modify_status(self, chat_id, status):
        connection = self.pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute('UPDATE subscriptions SET status=%s WHERE chat_id=%s', (status, str(chat_id)))
        connection.commit()
        self.pool.putconn(connection)

    def modify_user_id(self, chat_id, user_id):
        connection = self.pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute('UPDATE subscriptions SET user_id=%s WHERE chat_id=%s', (user_id, str(chat_id)))
        connection.commit()
        self.pool.putconn(connection)

