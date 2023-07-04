from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

def db_connect():
    while True:
        try:
            con = psycopg2.connect(host=settings.database_host, database=settings.database_name, user=settings.database_username,
                                   password=settings.database_password, cursor_factory=RealDictCursor)
            cursor = con.cursor()
            print('Database connected')
            return con, cursor
        except Exception as p:
            print('fail to connect to database')
            print(f'Error: {p}')
            sleep(1)

def db_close(con):
    con.commit()
    con.close()
    print('Database disconnected')