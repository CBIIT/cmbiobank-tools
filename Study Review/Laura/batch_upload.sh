#!/bin/bash

DATABASE_NAME="ravedata"
USERNAME="amohandas"
PASSWORD="amWy3QZJ#"
FILES_PATH="/Users/mohandasa2/Library/CloudStorage/OneDrive-SharedLibraries-NationalInstitutesofHealth/NCI-DCTD\ Moonshot\ Bioban$
General/Rave\ Data\ Dumps/10323_4200_20230806_060000"

for file in "$FILES_PATH"/*.csv; do
    table_name=$(basename "$file" .csv)
    mysql -u "$USERNAME" -p"$PASSWORD" "$DATABASE_NAME" -e "LOAD DATA INFILE '$file' INTO TABLE $table_name FIELDS TERMINATED BY $
IGNORE 1 LINES;"
done