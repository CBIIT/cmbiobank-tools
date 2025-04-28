import os
import mysql.connector

# Function to load CSV files into MySQL
def load_csv_files_to_mysql(directory_path, mysql_host, mysql_user, mysql_password, mysql_database):
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    # Iterate through CSV files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            print(filename)
            # MySQL table name (use filename without extension)
            table_name = os.path.splitext(filename)[0]

            # Full path to CSV file
            csv_file_path = os.path.join(directory_path, filename)

            # Execute the LOAD DATA INFILE statement
            load_data_query = f"""
                LOAD DATA INFILE '/Users/mohandasa2/Desktop/Laura-study/RAVE/csv/'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS; -- Skip header row if present
            """

            try:
                # Execute the query
                cursor.execute(load_data_query)

                # Commit changes
                connection.commit()
                print(f"Data from {csv_file_path} loaded into {table_name} successfully.")
            except mysql.connector.Error as err:
                # Handle errors
                print(f"Error loading data from {csv_file_path} into {table_name}: {err}")
                connection.rollback()

    # Close cursor and connection
    cursor.close()
    connection.close()

# Example usage:
directory_path = "/Users/mohandasa2/Desktop/Laura-study/RAVE/csv/"  # Path to the directory containing CSV files
mysql_host = 'ctos-data-team.org'
mysql_user = 'anita'
mysql_password = 'a1n1taP@ss'
mysql_database = 'cmb'

load_csv_files_to_mysql(directory_path, mysql_host, mysql_user, mysql_password, mysql_database)
