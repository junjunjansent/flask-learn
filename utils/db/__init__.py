import psycopg2
import os


def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(db_url)
    # connection = psycopg2.connect(
    #     host='localhost', 
    #     database='flask_auth_db',
    #     user=os.getenv('POSTGRES_USERNAME'),
    #     password=os.getenv('POSTGRES_PASSWORD'))
    return connection

def get_db_connection1():
    db_url = os.getenv('DATABASE_URL')
    connection = psycopg2.connect(db_url)
    # connection = psycopg2.connect(
    #     host='localhost', 
    #     database='flask_auth_db',
    #     user=os.getenv('POSTGRES_USERNAME'),
    #     password=os.getenv('POSTGRES_PASSWORD'))
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return (connection, cursor) # better to return tuple to maintain order