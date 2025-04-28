
import os
import mysql.connector
import csv

# MySQL database configuration
host = 'biobank-dev-db.cc2msjsimutx.us-east-1.rds.amazonaws.com'
user = 'amohandas'
password = 'amWy3QZJ#'
database = 'ravedata'
port = '3306'
#
# # Folder path containing CSV files
# csv_folder = "/Users/mohandasa2/Desktop/Laura-study/Test/val"

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)

cursor = connection.cursor()

if connection.is_connected():
    print("Connection established.")
else:
    print("Connection failed.")


# # Create a table
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS students (
#     id INT
#     AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     age INT
# );
# '''

# Path to the CSV file
csv_file_path = '/Users/mohandasa2/Desktop/Laura-study/Test/val/oncomine_result.csv'  # Change to your CSV file path

# Table name in MySQL
table_name = 'testing'

# Load CSV data into MySQL
load_query = f"LOAD DATA INFILE '{csv_file_path}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' IGNORE 1 LINES"
cursor.execute(load_query)



#
# cursor.execute(create_table_query)
#
# # Insert values into the table
# insert_data_query = '''
# INSERT INTO students (name, age)
# VALUES (%s, %s);
# '''
#
# # Values to insert
# students_data = [
#     ('Alice', 22),
#     ('Bob', 21),
#     ('Charlie', 23)
# ]
#
# # Insert each row of data
# for student in students_data:
#     cursor.execute(insert_data_query, student)

# Iterate through CSV files in the folder
# for csv_file in os.listdir(csv_folder):
#     if csv_file.endswith('.csv'):
#         print(csv_file)
#         table_name = os.path.splitext(csv_file)[0]
#         csv_path = os.path.join(csv_folder, csv_file)
#
#         # Construct LOAD DATA INFILE query
#         query = f"LOAD DATA INFILE '{csv_path}' INTO TABLE {table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n' IGNORE 1 LINES;"
#
#         # Execute the query
#         cursor.execute(query)
#         connection.commit()
# Close the cursor and connection
cursor.close()
connection.close()
