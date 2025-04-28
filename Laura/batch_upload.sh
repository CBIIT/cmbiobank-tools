#!/bin/bash

host = 'ctos-data-team.org'
DATABASE_NAME="cmb"
USERNAME="anita"
PASSWORD="a1n1taP@ss"
FILES_PATH="/Users/mohandasa2/Desktop/Laura-study/RAVE/csv/"

for file in "$FILES_PATH"/*.csv; do
    table_name=$(basename "$file" .csv)
    mysql -u "$USERNAME" -p"$PASSWORD" "$DATABASE_NAME" -e "LOAD DATA INFILE '$file' INTO TABLE $table_name FIELDS TERMINATED BY $
IGNORE 1 LINES;"
done