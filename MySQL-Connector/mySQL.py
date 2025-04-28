
import os
import mysql.connector

import csv

# MySQL database configuration
host = 'ctos-data-team.org'
user = 'anita'
password = 'a1n1taP@ss'
database = 'cmb'
port = '3306'
auth_plugin = 'mysql_native_password'

#
# Folder path containing CSV files
csv_folder = "/Users/mohandasa2/Desktop/Laura-study/RAVE/csv/"

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port,
    auth_plugin=auth_plugin
)

cursor = connection.cursor()

if connection.is_connected():
    print("Connection established.")
else:
    print("Connection failed.")

#
# cursor.execute("SHOW TABLES")
#
# # Fetch all table names
# table_names = cursor.fetchall()
#
# # Iterate through the result set and print table names
# for name in table_names:
#     print(name[0])



# Iterate through CSV files in the folder
for csv_file in os.listdir(csv_folder):
    if csv_file.endswith('.csv'):
        table_name = os.path.splitext(csv_file)[0]
        csv_path = os.path.join(csv_folder, csv_file)
    else:
        print(csv_file)

# Construct LOAD DATA INFILE query
query = f"LOAD DATA LOCAL INFILE '{csv_folder}' into table enrollment FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' IGNORE 1 LINES;"
 # Execute the query
cursor.execute(query)
connection.commit()
# Close the cursor and connection
cursor.close()
connection.close()
