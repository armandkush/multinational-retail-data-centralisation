import psycopg2

# Database connection details
db_host = 'data-handling-project-readonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com'
db_user = 'aicore_admin'
db_password = 'AiCore2022'
db_name = 'postgres'
db_port = 5432

# Establish a connection to the database
try:
    connection = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port
    )

    # Create a cursor for executing SQL queries
    cursor = connection.cursor()

    # Example query: List all tables in the public schema
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()

    # Print the list of tables
    print("Tables in the 'public' schema:")
    for table in tables:
        print(table[0])

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

except Exception as e:
    print(f"Error connecting to the database: {str(e)}")