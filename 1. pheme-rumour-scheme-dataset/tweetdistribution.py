import os
import csv
import pytz
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from collections import defaultdict


# Data structure to store a tweet
class Tweet:
    def __init__(self, tweet_id, type, timestamp, misinformation=None, true=None, reply_to=None):
        self.tweet_id = tweet_id    # Tweet ID
        self.type = type            # Indicates source tweet or reply
        self.timestamp = timestamp  # Timestamp (converted to Amsterdam time) of when the tweet was created
        self.misinformation = misinformation    # Indicates if the tweet is later proven to be misinformation
        self.true = true            # Indicates if a tweet is later proven to be true
        self.reply_to = reply_to    # ID of the parent tweet

    # Representation of tweet when printing
    def __str__(self):
        return f'Tweet with ID {self.tweet_id}: type={self.type}, timestamp={self.timestamp}, misinformation={self.misinformation}, true={self.true} reply_to={self.reply_to}'


### Global variables

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'
ottawa = 'ottawashooting'

# Pick a folder
FOLDER = german_airplane

current_directory = os.getcwd()

# Target timezone (Amsterdam)
amsterdam_tz = pytz.timezone('Europe/Amsterdam')


# Network of tweets
T = nx.Graph()
Tw = nx.Graph()


# Retrieve the timestamp given by a file in the folder
def get_timestamp(folder):
    """
    Function to get the timestamp given by current folder
    """
    for root, dirs, files in os.walk(folder):
        if "source-tweet" in root:
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    created_at = data["created_at"]
                    utc_time = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")

                    return utc_time


# Add reaction to network G and place edge between reaction and its parent
def add_reaction_tweet(G, parent, tweet_id, t_stamp):
    G.add_node(tweet_id, color = 'black', timestamp = t_stamp)

    # Place edge
    G.add_edge(parent, tweet_id)


# Add the right color to the tweet
def add_source_tweet(G, source_tweet, t_stamp, misinfo, true):
    c = "yellow"

    if misinfo and true:    # Uncertain
        c = 'blue'
    elif misinfo:
        c = "red"
    elif true:
        c = 'green'
    else:                   # Also Uncertain
        c = 'blue'    
    
    G.add_node(source_tweet, color = c, timestamp = t_stamp)

        

# Export 
# This function is from Bachelor Thesis of Joy Kwant
def position_to_csv(pos, graph_name):
    """ Exports dictionary of positions of node, created by NetworkX spring_layout.
    @param pos: position disctionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open('pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))


# Import
# This function is from Bachelor Thesis of Joy Kwant
def csv_dict_position(pos, graph_name):
    """ Imports the position dictionary, for each node there is a x,y-coordinate.
    @param pos: empty position dictionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open('pos_dic_'+ graph_name + '.csv', newline='') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            pos.setdefault(row[0])
            pos[row[0]] = [float(row[1]), float(row[2])]    



# Function to find the source tweet's misinformation and true values for a reply tweet
def find_source_info(tweet_id, tweets_dict):
    # Start from the given tweet and traverse up the chain to find the source tweet
    current_tweet = tweets_dict.get(tweet_id)

    # Traverse until you find the source tweet
    while current_tweet:
        if current_tweet.type == 'source':
            return current_tweet.misinformation, current_tweet.true  # Found source tweet, return its info
        
        # Move to the parent tweet (reply_to)
        current_tweet = tweets_dict.get(current_tweet.reply_to)

    # No source tweet was found
    return None, None


# Add the reply to the dictionary of the type of the source-tweet
def add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter):    
    # Find misinformation and true values for a specific reply tweet (e.g., tweet 3)
    is_misinfo, is_true = find_source_info(tweet_id=tweet.tweet_id, tweets_dict=tweets_dict)

    if is_misinfo and is_true:
        # Uncertain 
        uncertain_dict[current_iter].append(tweet.tweet_id,)
    
    elif is_misinfo:
        misinfo_dict[current_iter].append(tweet.tweet_id,)
        
    elif is_true:
        true_dict[current_iter].append(tweet.tweet_id,)
    
    else:
        # Also uncertain
        uncertain_dict[current_iter].append(tweet.tweet_id,)


# Add the tweet to the network G
def add_tweet_to_network(G, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iter):
    # Add the tweet to the graph
    if tweet.type == "source":
        # print("source tweet")
        add_source_tweet(G, source_tweet=tweet.tweet_id, t_stamp=tweet.timestamp, misinfo=tweet.misinformation, true=tweet.true)
    else:   # Reply tweet
        # print("reaction")
        add_reaction_tweet(G, parent=tweet.reply_to, tweet_id=tweet.tweet_id, t_stamp=tweet.timestamp)
        add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter)

            
# Plot the graph of netwrok G
def plot_graph(G, network):
    fig, ax = plt.subplots(figsize=(12, 7))

    # Fetch the positions of the nodes in the csv of the network of the FOLDER
    pos = {} 
    csv_dict_position(pos, FOLDER + "_" + network)

    # Keep track of the nodes that are extra in the current network than that of the csv file
    nodes_to_remove = []
    for n in G.nodes():
        if n not in pos.keys():
            nodes_to_remove.append(n)

    # Remove those extra nodes from the current network
    G.remove_nodes_from(nodes_to_remove)   
    
    # print(f" Nodes in the graph:  {G.number_of_nodes()} ")
    # print(len(pos.keys())) 
    
    node_color = [G.nodes[n]['color'] for n in G.nodes]

    # Draw network
    nx.draw_networkx(
            G,
            pos = pos,
            with_labels = False,
            node_color = node_color,
            node_size = 20,
            edge_color = "gainsboro",
            alpha = 0.4,
        )


    # Create a legend using mpatches for the source and reply colors
    misinfo_patch = mpatches.Patch(color='red', label='Misformation')
    facts_patch = mpatches.Patch(color='green', label='Facts')
    uncertain_patch = mpatches.Patch(color='blue', label='Uncertain')
    reply_patch = mpatches.Patch(color='black', label='Reply Tweet')
    plt.legend(handles=[misinfo_patch, facts_patch, uncertain_patch, reply_patch])



    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    ax.set_title(f"Folder: {FOLDER}, network of {network}", font)
    # Change font color for legend
    font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")

    #plt.show()



# The bar plot for the types misinformation, true and uncertain, showing for each iteration
def plot_barplot(misinfo_dict, true_dict, uncertain_dict, max_iter):
    # List of with all iterations
    all_iterations = list(range(1, max_iter + 1))

    # Prepare the values for each iteration, filling in zeros where necessary
    misinfo_values = [misinfo_dict.get(i, 0) for i in all_iterations]
    true_values = [true_dict.get(i, 0) for i in all_iterations]
    uncertain_values = [uncertain_dict.get(i, 0) for i in all_iterations]

    bar_width = 0.25  # Width of each bar
    indices = np.arange(max_iter)  # The position on the x-axis for each group of bars

    # Create a bar plot
    fig, ax = plt.subplots()

    # Plot the bars for each category, shifting their positions by bar_width
    p1 = ax.bar(indices - bar_width, misinfo_values, bar_width, label='Misinformation', color='red')
    p2 = ax.bar(indices, true_values, bar_width, label='True', color='green')
    p3 = ax.bar(indices + bar_width, uncertain_values, bar_width, label='Uncertain', color='blue')

    # Labeling
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Number of Replies')
    ax.set_title(f'Number of Replies per Iteration of {FOLDER}')
    ax.set_xticks(indices)
    ax.set_xticklabels([f't={i}' for i in all_iterations])
    ax.legend()

    # Show plot
    plt.tight_layout()
    plt.show()




##### MAIN


### First loop: Getting the first timestamp of event
first_timestamp = None

# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    
    if FOLDER in root:
        first_folder = os.path.join(root, dirs[0])  # First folder
        first_timestamp = get_timestamp(first_folder)

        break

last_timestamp = first_timestamp


### Second loop: Appending the source tweets and reaction to the list of all Tweets
tweets = []
is_misinfo = None
is_true = None

# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    if FOLDER in root:        
        # First loop goes through seperate files
        for file in files:
            # Full file path
            file_path = os.path.join(root, file)

            if "annotation.json" in file_path:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    is_misinfo = data['misinformation']
                    if 'true' in data:
                        is_true = data['true']

        # Second through the reaction folder
        if "reaction" in root:
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    id = data["id_str"] # Tweet ID
                    parent = str(data["in_reply_to_status_id"]) # Parent node
                    created_at = data["created_at"]
                    user_data = data.get('user', {})  # Get 'user' data, or an empty dict if it doesn't exist
                    time_zone = user_data.get('time_zone', 'NaN')
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")

                    # Add tweet to the list of tweets
                    tweets.append(Tweet(tweet_id=id, type="reply", timestamp=time_stamp_utc0, reply_to=parent))
                    
                    # Check if this tweet is later than the currently found last tweet
                    if time_stamp_utc0 > last_timestamp:
                        last_timestamp = time_stamp_utc0
                   
        # Lastly through the source-tweet folder
        if "source-tweet" in root:
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    id = data["id_str"]
                    created_at = data["created_at"]
                    user_data = data.get('user', {})  # Get 'user' data, or an empty dict if it doesn't exist
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")

                    # Add tweet to the list of tweets
                    tweets.append(Tweet(tweet_id=id, type="source", timestamp=time_stamp_utc0, misinformation=is_misinfo, true=is_true))

                    # Reset the info for next thread folder
                    is_misinfo = None
                    is_true = None

                    # Check if this tweet is later than the currently found last tweet
                    if time_stamp_utc0 > last_timestamp:
                        last_timestamp = time_stamp_utc0



# ###########################################################################################################################
# Sort tweets on timestamp
tweets.sort(key=lambda tweet: tweet.timestamp)

# Dictionary for tweets for the barplots
tweets_dict = {tweet.tweet_id: tweet for tweet in tweets}

# # Based on the timestamps of the first and last tweet, determine the iteration duration
max_iter = 5
iteration_duration = (last_timestamp - first_timestamp)/max_iter

misinfo_dict = defaultdict(list)
true_dict = defaultdict(list)
uncertain_dict = defaultdict(list)

current_iteration = 1   # Start at iteration 1
# Keep track of iterations
for tweet in tweets:
    # First check if the tweet is outside of the current iteration window, plot the graph and increase iteration
    if tweet.timestamp > ((current_iteration * iteration_duration) + first_timestamp):
        # Check if the tweet fits in the next iteration, otherwise iterate even further
        for i in range(5):
            if tweet.timestamp >= (((current_iteration + i) * iteration_duration) + first_timestamp):
                # Plot current iteration and increase iteration counter
                plot_graph(Tw, "tweets")
                current_iteration += 1
    # Then decide what to do with the tweet
    # If this tweet is on the upper boundary of the iteration, add the tweet to the iteration first, then plot
    if tweet.timestamp == ((current_iteration * iteration_duration) + first_timestamp):
        # Add tweet (== so still belongs to the current iteration)
        add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)
        # Then plot current iteration and increase iteration counter
        plot_graph(Tw, "tweets")
        current_iteration += 1
    else :      # Tweet belongs in current iteration, add tweet then continue on to the next tweet
        # Add tweet to current iteration
        add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)


# Dictionaries for barplots
misinfo_dict = {key: len(value) for key, value in misinfo_dict.items()}
true_dict = {key: len(value) for key, value in true_dict.items()}
uncertain_dict = {key: len(value) for key, value in uncertain_dict.items()}

# Barplots
plot_barplot(misinfo_dict, true_dict, uncertain_dict, max_iter)



###########################################################################################################################


# t = iter (start 0)
# LOOP 2: Per Folder van een source tweet
    # convert time to amsterdam time
    # tweet_time = timestamp - tweet start
    # 
    # Checken hoort die bij current iter (tweet_time (- tweet_start?) <(=?) t * iteration_duration + tweet_start)
        # - Ja : voeg toe aan Graph
        # - Nee: Plotten we current graph
        #        increase iter
        #        toevoegen aan (new current) graph


# print(f"First time: {first_timestamp}")
# print(f"Last time: {last_timestamp}")
# iter_duration = (last_timestamp - first_timestamp)/5
# print(f"iter duration {iter_duration}")
# t1_start = first_timestamp + iter_duration
# if first_timestamp > t1_start:
#     print("jippieeeeee")
# else:
#     print("oh nooooo")
# # print(f"start of t1: {first_timestamp + iter_duration}")

# # print(first_timestamp + ((last_timestamp - first_timestamp)/5))



# LOOP 1: voor 1ste een laaste tijd

# 10 iteration berekenen  -->> [t0, t1, t2, t3]

# begintime of t_iter = iter * duration + tweet_start


# TODO:
# - MISINFORMATION or TRUE colors
# - Plots 
# - Graphs
# - Reactions?

# Tweet (node)
# - ID
# - source tweet/reply 
# - (misinformation, true): misinformation (1,0) / true (0,1) / uncertain (0,0), (1,1)
# - colour
#       - source tweet -> misinformation -> colour red/green
#       - reply -> colour black
# - converted time stamp
# - in reply to

# Barplot
# - source tweet/reply 
# - (misinformation, true): misinformation (1,0) / true (0,1) / uncertain (0,0), (1,1)
# - colour
# - 3 lists of tuples (backup option = 6 arrays)
#       misinformation  =  [(source, reply)]
#       true            =  [(source, reply)]
#       uncertain       =  [(source, reply)]
#
#       example = [(2, 0), (3, 2), (5, 4), (6, 10), ...]
#                    t0      t1      t2      t3     t..
# what is t?
# t0 = starting point (first tweet)
# t_max (max iter) = end point (final tweet)
# number of iterations (= 5? 10?)
# time per iteration = t_max-t0/number of iterations

# For (t0 -> tmax)
#   if t < t_iteration
#       add nodes within iteration
#       draw iteration