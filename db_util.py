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