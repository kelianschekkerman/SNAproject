import os

# Base directory (e.g., Folder A)
base_directory = r'C:\Users\..\gitlab\SNAproject\1. pheme-rumour-scheme-dataset'


# Loop through the folders and subfolders
# Example 
# root:  C:\Users\Joy-k\Downloads\Uni\Y2P1 - Social Network Analysis\1. pheme-rumour-scheme-dataset\threads\en\charliehebdo\553461741917863936
# dirs:  ['images', 'reactions', 'source-tweets', 'urls-content']
for root, dirs, files in os.walk(base_directory):
    print('root: ', root)
    print('dirs: ',dirs) 
    for file in files:
        # Full file path
        file_path = os.path.join(root, file)
        print(file_path)
