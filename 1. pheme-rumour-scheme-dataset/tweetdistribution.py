import os
import pytz
import json
from datetime import datetime
from get_timezones import timezone_map  # Timezone map to match strings to pytz timezones

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

# Pick a folder
FOLDER = putin

current_directory = os.getcwd()

# Target timezone (Amsterdam)
amsterdam_tz = pytz.timezone('Europe/Amsterdam')

# Function to convert time to the desired timezone
def convert_to_amsterdam(timestamp_str, original_tz_str):
    # Parse the original time string into a datetime object
    dt = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S +0000 %Y')

    # Determine the original timezone
    if original_tz_str and original_tz_str in timezone_map:
        original_tz = pytz.timezone(timezone_map[original_tz_str])
    else:
        # Default to UTC if timezone is None or not in the map
        original_tz = pytz.utc
    
    # Localize the datetime object to the original timezone
    localized_dt = original_tz.localize(dt)
    
    # Convert the datetime to Amsterdam timezone
    amsterdam_time = localized_dt.astimezone(amsterdam_tz)
    
    return amsterdam_time


# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    if FOLDER in root:
        
        for file in files:
            # Full file path
            file_path = os.path.join(root, file)

            if "annotation.json" in file_path:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    is_rumour_info = data['is_rumour']
                    print(is_rumour_info)
                    is_misinfo = data['misinformation']
                    print(f"is {is_rumour_info} and misformation: {is_misinfo}")
                    if 'true' in data:
                        is_true = data['true']
                        print(f"true: {is_true}")

        if "source-tweet" in root:
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    id = data["id_str"]
                    
                    created_at = data["created_at"]
                    user_data = data.get('user', {})  # Get 'user' data, or an empty dict if it doesn't exist
                    time_zone = user_data.get('time_zone', 'NaN')
                    print(f"{id} : {created_at}, {time_zone}") 

                    ## Converting
                    amsterdam_time = convert_to_amsterdam(created_at, time_zone)
                    print(f"ID: {id}, Amsterdam Time: {amsterdam_time}\n")