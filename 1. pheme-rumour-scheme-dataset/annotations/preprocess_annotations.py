def filter_tweets_by_event(input_file, output_file, events_to_keep):
    # Open input file to read from and create an output file to write to
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        keep_tweet = False
        
        for line in infile:
            # Check if the line marks the start of a section or a tweet, indicated by #
            if line.startswith("#"):
                outfile.write(line)
                keep_tweet = False
            elif '"event":' in line:
                # Check if the tweet is from the EU events
                for event in events_to_keep:
                    if f'"event":"{event}"' in line:
                        keep_tweet = True   # Keep EU events
                        break
                else:
                    keep_tweet = False      # Discard non-EU events

            # If the tweet matches the event criteria, write it to the output file
            if keep_tweet:
                outfile.write(line)

input_file = 'en-scheme-annotations.json'       # Annotation scheme from dataset
output_file = 'filtered_annotations.json'
events_to_keep = {"germanwings-crash", "charliehebdo", "putinmissing"}      # EU events that we want to keep

# Filter all non-EU events and save the new annotation scheme to a new file
filter_tweets_by_event(input_file, output_file, events_to_keep)
