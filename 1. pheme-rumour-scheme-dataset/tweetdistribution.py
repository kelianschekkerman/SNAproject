import os
import json

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

# Pick a folder
FOLDER = charlie

current_directory = os.getcwd()


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