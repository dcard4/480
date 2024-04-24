import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def create_database(db_params, sql_schema_file):
    """Create a database and initialize it with a schema from an SQL file"""
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cur = conn.cursor()
    with open(sql_schema_file, 'r') as f:
        sql = f.read()
        cur.execute(sql)
    cur.close()
    conn.close()

def create_connection(db_params):
    """Create a database connection to the PostgreSQL database specified by db_params"""
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
    except psycopg2.Error as e:
        print("Connection error: ", e)
    return conn

def add_client(conn, email, password, name):
    """Add a new client into the Clients table"""
    sql = sql.SQL('''INSERT INTO Clients(email, name, password)
                     VALUES (%s, %s, %s)''')
    try:
        cur = conn.cursor()
        cur.execute(sql, (email, name, password))
        conn.commit()
        cur.close()
    except psycopg2.IntegrityError as e:
        print("Error:", e)

def main():
    db_params = {
        'dbname': 'your_library',
        'user': 'username',
        'password': 'password',
        'host': 'localhost'
    }
    sql_schema_file = "library.sql"  # Path to your SQL file with the schema

    # Create and initialize the database
    create_database(db_params, sql_schema_file)

    # Create a database connection
    conn = create_connection(db_params)

    if conn is not None:
        email = input("Enter your email: ")
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        # Add a client
        add_client(conn, email, password, name)

        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
