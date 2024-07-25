
import pymysql

host = 'aerodata.cnlxiych4bri.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'forest-tree-baked'
database = 'aerodata'

connection = None

try:
    # Establish a connection to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    print('Connection created!')

    # Create a cursor object to interact with the database
    with connection.cursor() as cursor:
        # Execute SQL queries or database operations here

        # Example: Execute a SELECT query
        cursor.execute("SELECT * FROM your_table_name")
        results = cursor.fetchall()
        for row in results:
            print(row)

except Exception as e:
    print("Error: {}".format(e))
finally:
   # Close the database connection when done
    if connection is not None:
        connection.close()