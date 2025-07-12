from db import get_db_connection1


def create_tables():
    connection, cursor = get_db_connection1()
    