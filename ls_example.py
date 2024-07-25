import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'admin',
    'password': 'forest-tree-baked',
    'host': 'aerodata.cnlxiych4bri.us-east-2.rds.amazonaws.com',
    'database': 'aerodata',
    'raise_on_warnings': True
}

cursor = None
conn = None

try:
    # Establishing the connection
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Listing all tables
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()
