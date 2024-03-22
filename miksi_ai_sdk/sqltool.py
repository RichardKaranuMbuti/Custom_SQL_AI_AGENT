import pymysql
import pymysql.cursors
import os
import openai
import json


db_name = None
db_user = None
db_password = None
db_host = None
db_port = 3306


# This function accepts mySQL db credentials and an sql query and executes it 
def get_db_connection(db_user, db_password, db_host, db_port, db_name):
    """
    Establishes and returns a connection to the MySQL database.

    The database credentials are hardcoded in this function. In a real-world scenario,
    it's better to use environment variables or a configuration file to handle credentials securely.

    :return: A pymysql connection object
    """
    db_credentials = {
        'host': db_host,
        'user': db_user,
        'password': db_password,
        'database': db_name,
        'port': db_port,  # Update with your db port
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        connection = pymysql.connect(**db_credentials)
        return connection
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None


def get_database_schema():
    """
    Retrieves the schema (tables and columns with types) of the specified database using a connection established by get_db_connection.
    """
    schema_info = {}
    try:
        connection = get_db_connection(db_user, db_password, db_host, db_port, db_name) # pass these as global variables
        if connection is None:
            return None

        with connection.cursor() as cursor:
            # Fetching all table names in the database
            tables_query = "SHOW TABLES"
            cursor.execute(tables_query)
            tables = cursor.fetchall()

            for table in tables:
                # The key for table names in the result might vary, so adjust as needed
                table_name = list(table.values())[0]
                schema_info[table_name] = []

                # Fetching all column names and types for a table
                columns_query = f"SHOW COLUMNS FROM {table_name}"
                cursor.execute(columns_query)
                columns = cursor.fetchall()

                for column in columns:
                    column_info = {
                        "name": column["Field"],
                        "type": column["Type"]
                    }
                    schema_info[table_name].append(column_info)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return schema_info


def set_database_config(name, user, password, host, port):
    """
    Updates the global database configuration variables.
    
    Args:
    - name: The name of the database.
    - user: The username for the database.
    - password: The password for the database.
    - host: The host of the database.
    - port: The port number for the database connection.
    
    Raises:
    - ValueError: If any of the arguments is None or if port is not an integer.
    """
    global db_name, db_user, db_password, db_host, db_port
    
    # Check for None values and port being an integer
    if None in (name, user, password, host) or not isinstance(port, int):
        raise ValueError("All parameters must be provided and 'port' must be an integer.")
    
    # Update global variables
    db_name = name
    db_user = user
    db_password = password
    db_host = host
    db_port = port

def check_db_config_variables():
    """
    Checks the global database configuration variables for None, null, or empty values.
    
    Returns:
    - A list of variable names that are None, null, or empty.
    """
    # List of variable names and their values
    variables = {
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password,
        'db_host': db_host,
        'db_port': db_port
    }
    
    # Check for None, null, or empty values
    invalid_vars = [name for name, value in variables.items() if value is None or value == '']
    if invalid_vars:
        print("The following configuration variables are invalid:", ', '.join(invalid_vars))
    else:
        print("All configuration variables are set correctly.")
    
    return invalid_vars

#db_info = get_database_schema()
#print(db_info)

def execute_query(sql_query):
    """
    Executes the given SQL query using the database connection established by get_db_connection.

    :param sql_query: SQL query to be executed
    :return: Query results or None if an error occurs
    """
    try:
        connection = get_db_connection(db_user, db_password, db_host, db_port, db_name) # pass these as global variables
        if connection is None:
            return None

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None
    finally:
        if connection:
            connection.close()




