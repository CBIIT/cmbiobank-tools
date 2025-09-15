import os
import pandas as pd
from sqlalchemy import create_engine

# Function to load CSV files into MySQL using SQLAlchemy
def load_csv_to_mysql(csv_dir, engine):
    for file_name in os.listdir(csv_dir):
        if file_name.endswith(".CSV"):
            table_name = os.path.splitext(file_name)[0]  # Extract table name from file name
            csv_path = os.path.join(csv_dir, file_name)
            df = pd.read_csv(csv_path)
            try:
                df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
                print(f"Loaded {file_name} into MySQL")
            except Exception as e:
                print(f"Error loading {file_name} into MySQL: {e}")

# MySQL database connection parameters
host = 'biobank-dev-db.cc2msjsimutx.us-east-1.rds.amazonaws.com'
database = 'ravedata'
user = 'amohandas'
password = 'amWy3QZJ#'

# Create MySQL connection engine using SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Directory containing CSV files
csv_directory = '/Users/mohandasa2/Library/CloudStorage/OneDrive-SharedLibraries-NationalInstitutesofHealth/NCI-DCTD Moonshot Biobank IT (O365) - General/Rave Data Dumps/10323_4200_20240610_133000'

# Load CSV files into MySQL using SQLAlchemy engine
load_csv_to_mysql(csv_directory, engine)
