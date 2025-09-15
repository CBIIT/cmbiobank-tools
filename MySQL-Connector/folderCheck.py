import os
from datetime import datetime, timedelta
import time

# Directory to monitor
directory_path = "/Users/mohandasa2/Library/CloudStorage/OneDrive-SharedLibraries-NationalInstitutesofHealth/NCI-DCTD Moonshot Biobank IT (O365) - General/Rave Data Dumps"


# Function to check for a new folder every Monday
def check_for_new_folder():
    while True:
        # Check if today is Monday
        today = datetime.now()
        if today.weekday() == 1:  # Monday is represented by 0
            # List all directories in the specified directory
            directories = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

            # Check if there's a new directory created
            for dir_name in directories:
                if dir_name.startswith("10323"):
                    dir_path = os.path.join(directory_path, dir_name)
                    created_time = os.path.getctime(dir_path)
                    created_date = datetime.fromtimestamp(created_time)

                    if created_date.date() == today.date():
                        print(f"A new folder '{dir_name}' was created today ({today.strftime('%Y-%m-%d')}).")
                else:
                    continue
                    # You can add further actions here if needed

        # Sleep for 24 hours before checking again
        time.sleep(24 * 60 * 60)  # Sleep for 24 hours (in seconds)


# Start checking for new folders
check_for_new_folder()
