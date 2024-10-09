import os

# Get the current working directory
current_directory = os.getcwd()

# Loop through the folders and subfolders
# Example 
# root:  \SNAProject\1. pheme-rumour-scheme-dataset\threads\en\charliehebdo\553461741917863936
# dirs:  ['images', 'reactions', 'source-tweets', 'urls-content']
for root, dirs, files in os.walk(current_directory):
    print('root: ', root)
    print('dirs: ',dirs) 
    for file in files:
        # Full file path
        file_path = os.path.join(root, file)
        print(file_path)
