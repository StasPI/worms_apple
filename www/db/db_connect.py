from sqlalchemy import create_engine

type_db = 'postgresql'
driver_db = 'psycopg2'
user_name_db = 'postgres'
password_db = 'testpass'
host_db = 'localhost'
port_db = '5432'
name_db = 'www'


def db_engine():
    return create_engine(
        f'{type_db}+{driver_db}://{user_name_db}:{password_db}@{host_db}:{port_db}/{name_db}',
        echo=True)
