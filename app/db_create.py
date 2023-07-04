import psycopg2
from .config import settings

db_name = settings.database_name

def main():
    conn = psycopg2.connect(
    database=settings.main_database,
        user=settings.database_username,
        password=settings.database_password,
        host=settings.database_host,
        port=settings.database_port
    )

    conn.autocommit = True
 
    # Creating a cursor object
    cursor = conn.cursor()
 
    # executing query to create a database
    cursor.execute(f'CREATE database {db_name}')
    print("Database has been created successfully !!")
 
    # Closing the connection

    conn.close()

if __name__ == '__main__':
    main()