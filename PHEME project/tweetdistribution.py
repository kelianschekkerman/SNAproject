import os
import csv
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

# Folders
charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'
ottawa = 'ottawashooting'

# Pick a folder
FOLDER = putin

# Current directory of where this file is stored
current_directory = os.getcwd()

# Network of tweets
T = nx.Graph()
Tw = nx.Graph()

# Two options for getting different information:
ITERATIONS_DISTRIBUTION = True
STATISTICS = True

# Global dictionary to track the retweets, favorite count and the number of reactions for each category
statistics = {
    'misinformation': defaultdict(list),
    'true': defaultdict(list),
    'uncertain': defaultdict(list)
}

def get_timestamp(folder):
    """
    Function to get the timestamp of the source in the current folder.

    @param folder: the current folder.
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


def add_reaction_tweet(G, parent, tweet_id, t_stamp):
    """
    Add reaction tweet to network G and place edge between reaction and its parent.

    @param G: The NetworkX Graph.
    @param parent: The ID of the parent tweet to which the tweet is reacting.
    @param tweet_id: The ID of the reaction tweet.
    """
    G.add_node(tweet_id, color = 'black', timestamp = t_stamp)

    # Place edge
    G.add_edge(parent, tweet_id)


def add_source_tweet(G, source_tweet, t_stamp, misinfo, true):
    """
    Add source tweet to network G with appropriate color based on misinformation and truth status.
    
    @param G: The NetworkX Graph.
    @param source_tweet: The ID of the source tweet.
    @param t_stamp: The timestamp of when the tweet was created.
    @param misinfo: A boolean indicating whether the tweet contains misinformation.
    @param true: A boolean indicating whether the tweet is true.
    """
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
 

# This function is from Bachelor Thesis of Joy Kwant
def position_to_csv(pos, graph_name):
    """ Exports dictionary of positions of node, created by NetworkX spring_layout.
    @param pos: position disctionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open(r'csv\pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))


# This function is from Bachelor Thesis of Joy Kwant
def csv_dict_position(pos, graph_name):
    """ Imports the position dictionary, for each node there is a x,y-coordinate.
    @param pos: empty position dictionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open(r'csv\pos_dic_'+ graph_name + '.csv', newline='') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            pos.setdefault(row[0])
            pos[row[0]] = [float(row[1]), float(row[2])]    


def find_source_info(tweet_id, tweets_dict):
    """
    Traverse the tweet chain to find the source tweet and retrieve its misinformation and truth values.
    
    @param tweet_id: The ID of the reply tweet for which to find the source tweet information.
    @param tweets_dict: A dictionary mapping tweet IDs to tweet objects.
    
    @return: A tuple containing the misinformation and truth values of the source tweet,
             or (None, None) if no source tweet is found.
    """
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


def add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter):
    """
    Add a reply tweet to the appropriate dictionary based on the source tweet's misinformation and truth values.
    
    @param misinfo_dict: A dictionary to store tweets identified as misinformation, organized by iteration.
    @param true_dict: A dictionary to store tweets identified as true, organized by iteration.
    @param uncertain_dict: A dictionary to store tweets identified as uncertain, organized by iteration.
    @param tweets_dict: A dictionary consisiting the tweet objects.
    @param tweet: The reply tweet object.
    @param current_iter: The current iteration for organizing tweets in the dictionaries.
    """    
    # Find misinformation and true values for a specific reply tweet (e.g., tweet 3)
    is_misinfo, is_true = find_source_info(tweet_id=tweet.tweet_id, tweets_dict=tweets_dict)

    if is_misinfo and is_true:
        # Uncertain 
        uncertain_dict[current_iter].append(tweet.tweet_id)
    
    elif is_misinfo:
        misinfo_dict[current_iter].append(tweet.tweet_id)
        
    elif is_true:
        true_dict[current_iter].append(tweet.tweet_id)
    
    else:
        # Also uncertain
        uncertain_dict[current_iter].append(tweet.tweet_id)


def add_tweet_to_network(G, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iter):
    """
    Add a tweet to the network graph G, distinguishing between source tweets and reply tweets.
    Also adds reply tweets to a specific dictionary with 'add_replies_to_dictionary'.
    
    @param G: The NetworkX Graph.
    @param tweet: The tweet object to be processed.
    @param misinfo_dict: A dictionary to store tweets identified as misinformation, organized by iteration.
    @param true_dict: A dictionary to store tweets identified as true, organized by iteration.
    @param uncertain_dict: A dictionary to store tweets identified as uncertain, organized by iteration.
    @param tweets_dict: A dictionary consisiting the tweet objects.
    @param current_iter: The current iteration for organizing tweets in the dictionaries.
    """
    # Add the tweet to the graph
    if tweet.type == "source":
        add_source_tweet(G, source_tweet=tweet.tweet_id, t_stamp=tweet.timestamp, misinfo=tweet.misinformation, true=tweet.true)
    else:   # Reply tweet
        add_reaction_tweet(G, parent=tweet.reply_to, tweet_id=tweet.tweet_id, t_stamp=tweet.timestamp)
        add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter)

            
def plot_graph(G, network, current_iteration, lower, upper):
    """
    Visualize the graph of network G using Matplotlib, based on node positions from a CSV file.
    
    @param G: The NetworkX Graph to be plotted.
    @param network: The name of the network, used to locate the corresponding position CSV file.
    @param current_iteration: The current iteration.
    @param lower: The lower limit for the time range displayed in the plot (first timestamp).
    @param upper: The upper limit for the time range displayed in the plot (last timestamp).
    """
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
    
    # Retrieve the node colors
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

    # Create a legend using mpatches for the three categories for the source tweets and reply colors
    misinfo_patch = mpatches.Patch(color='red', label='Misformation')
    facts_patch = mpatches.Patch(color='green', label='Facts')
    uncertain_patch = mpatches.Patch(color='blue', label='Uncertain')
    reply_patch = mpatches.Patch(color='black', label='Reply Tweet')
    plt.legend(handles=[misinfo_patch, facts_patch, uncertain_patch, reply_patch])

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    ax.set_title(f"Folder: {FOLDER}, network of {network}, iteration = {current_iteration}, times between {lower.strftime('%Y-%m-%d %H:%M')} and {upper.strftime('%Y-%m-%d %H:%M')}", font)
    # Change font color for legend
    font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")

    # Save the figure
    plt.savefig(os.path.join("../Graphs/tweet_distribution", f"tweet_dist_{FOLDER}_iter={current_iteration}"))


def plot_barplot(misinfo_dict, true_dict, uncertain_dict, max_iter, first_timestamp, last_timestamp, iteration_duration):
    """
    Generate a bar plot for the counts of misinformation, true, and uncertain replies across iterations.
    
    @param misinfo_dict: Dictionary with counts of misinformation replies per iteration.
    @param true_dict: Dictionary with counts of true replies per iteration.
    @param uncertain_dict: Dictionary with counts of uncertain replies per iteration.
    @param max_iter: The total number of iterations.
    @param first_timestamp: The starting timestamp of the event.
    @param last_timestamp: The ending timestamp of the event.
    @param iteration_duration: The duration of each iteration.
    """
    # List of with all iterations
    all_iterations = list(range(1, max_iter + 1))

    # Prepare the values for each iteration, filling in zeros where necessary
    misinfo_values = [misinfo_dict.get(i, 0) for i in all_iterations]
    true_values = [true_dict.get(i, 0) for i in all_iterations]
    uncertain_values = [uncertain_dict.get(i, 0) for i in all_iterations]

    bar_width = 0.25                # Width of each bar
    indices = np.arange(max_iter)   # The position on the x-axis for each group of bars

    # Create a bar plot
    fig, ax = plt.subplots()

    # Plot the bars for each category, shifting their positions by bar_width
    ax.bar(indices - bar_width, misinfo_values, bar_width, label='Misinformation', color='red')
    ax.bar(indices, true_values, bar_width, label='True', color='green')
    ax.bar(indices + bar_width, uncertain_values, bar_width, label='Uncertain', color='blue')

    # Format iteration_duration as hours, minutes, and seconds
    iteration_duration_str = ( f"{iteration_duration.days}d " if iteration_duration.days > 0 else ""
                            ) + f"{iteration_duration.seconds // 3600}h {iteration_duration.seconds % 3600 // 60}m {iteration_duration.seconds % 60}s"

    # Labeling
    ax.set_xlabel(f'Iteration (Duration is {iteration_duration_str})')
    ax.set_ylabel('Number of Replies')
    ax.set_title(f'Number of Replies per Iteration of {FOLDER}')
    ax.set_xticks(indices)
    ax.set_xticklabels([f't={i}' for i in all_iterations])

    # Add the first and last timestamps
    ax.annotate(f'Start: {first_timestamp.strftime("%Y-%m-%d %H:%M:%S")}',
            xy=(0, -0.15), xycoords=('data', 'axes fraction'),
            ha='center', va='top', fontsize=10, color='blue')

    ax.annotate(f'End: {last_timestamp.strftime("%Y-%m-%d %H:%M:%S")}',
            xy=(max_iter - 1, -0.15), xycoords=('data', 'axes fraction'),
            ha='center', va='top', fontsize=10, color='blue')

    ax.legend()
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(os.path.join("../Graphs/tweet_distribution/", f"barlot_tweets_{FOLDER}"))


def add_tweet_info(stat_dictionary, tweet_id, retweet_count, favorite_count, reaction_count):
    """
    Add tweet engagement statistics to the specified dictionary.
    
    @param stat_dictionary: The dictionary where tweet information will be stored.
    @param tweet_id: The ID of the source tweet being added.
    @param retweet_count: The number of retweets for the tweet.
    @param favorite_count: The number of favorites (likes) for the tweet.
    @param reaction_count: The total number of reactions for the tweet.
    """
    stat_dictionary[tweet_id] = {
        'retweet_count': retweet_count,
        'favorite_count': favorite_count,
        'reaction_count': reaction_count
    }


def add_to_statistic_dictionary(is_misinfo, is_true, tweet_id, retweet_count, favorite_count, reaction_count):
    """
    Add tweet engagement statistics to the specified dictionary.
    
    @param stat_dictionary: The dictionary where tweet information will be stored.
    @param tweet_id: The ID of the tweet being added.
    @param retweet_count: The number of retweets for the tweet.
    @param favorite_count: The number of favorites (likes) for the tweet.
    @param reaction_count: The total number of reactions (replies, etc.) for the tweet.
    """
    if is_misinfo and is_true:
        # Uncertain
        target_dict = statistics['uncertain']
    elif is_misinfo:
        target_dict = statistics['misinformation']
    elif is_true:
        target_dict = statistics['true']
    else:
        # Also uncertain
        target_dict = statistics['uncertain']

    add_tweet_info(target_dict, tweet_id, retweet_count, favorite_count, reaction_count)
    

def avg_comp_and_print(x, y, avg_string):
    """
    Calculate and print the average of x over y, with a specified description.
    
    @param x: The numerator for the average calculation.
    @param y: The denominator for the average calculation.
    @param avg_string: A string describing what is being averaged (e.g., "retweets").
    """
    avg_outcome = x / y if y > 0 else 0
    print(f"Average number of {avg_string} per source tweet   : {avg_outcome:.2f}") 


##### MAIN #####

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
reaction_count = 0

# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    if FOLDER in root:        
        # First loop goes through seperate files
        for file in files:
            # Full file path
            file_path = os.path.join(root, file)

            # Retrieve reliability information
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
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    reaction_count += 1

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
                    retweet_count = data["retweet_count"]
                    favorite_count  = data["favorite_count"]
                    created_at = data["created_at"]
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")

                    # Add tweet to the list of tweets
                    tweets.append(Tweet(tweet_id=id, type="source", timestamp=time_stamp_utc0, misinformation=is_misinfo, true=is_true))

                    # Add tweet to the appropriate statistics dictionary
                    add_to_statistic_dictionary(is_misinfo, is_true, id, retweet_count, favorite_count, reaction_count)

                    # Reset the info for next thread folder
                    is_misinfo = None
                    is_true = None
                    reaction_count = 0

                    # Check if this tweet is later than the currently found last tweet
                    if time_stamp_utc0 > last_timestamp:
                        last_timestamp = time_stamp_utc0

# Sort tweets on timestamp
tweets.sort(key=lambda tweet: tweet.timestamp)

# Dictionary for tweets for the barplots
tweets_dict = {tweet.tweet_id: tweet for tweet in tweets}

if ITERATIONS_DISTRIBUTION:
    # Based on the timestamps of the first and last tweet, determine the iteration duration
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
                    upper = (current_iteration * iteration_duration) + first_timestamp
                    lower = ((current_iteration - 1) * iteration_duration) + first_timestamp
                    plot_graph(Tw, "tweets", current_iteration, lower, upper)
                    current_iteration += 1
        # Then decide what to do with the tweet
        # If this tweet is on the upper boundary of the iteration, add the tweet to the iteration first, then plot
        if tweet.timestamp == ((current_iteration * iteration_duration) + first_timestamp):
            # Add tweet (== so still belongs to the current iteration)
            add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)
            # Then plot current iteration and increase iteration counter
            upper = (current_iteration * iteration_duration) + first_timestamp
            lower = ((current_iteration - 1) * iteration_duration) + first_timestamp
            plot_graph(Tw, "tweets", current_iteration, lower, upper)
            current_iteration += 1
        else :      # Tweet belongs in current iteration, add tweet then continue on to the next tweet
            # Add tweet to current iteration
            add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)

    # Dictionaries for barplots
    misinfo_dict = {key: len(value) for key, value in misinfo_dict.items()}
    true_dict = {key: len(value) for key, value in true_dict.items()}
    uncertain_dict = {key: len(value) for key, value in uncertain_dict.items()}

    # Barplots
    plot_barplot(misinfo_dict, true_dict, uncertain_dict, max_iter, first_timestamp, last_timestamp, iteration_duration)
    plt.show()

if STATISTICS:
    total_source_tweets = 0
    total_reactions = 0
    total_retweets = 0
    total_favorites = 0


    for category, tweets in statistics.items():
        print(f"Category: {category}")
        source_tweets = len(tweets)
        total_source_tweets += source_tweets

        reactions = retweets = favorites = 0

        # Loop through each tweet in the category
        for tweet_id, stats in tweets.items():            
            reactions += stats['reaction_count']
            retweets += stats['retweet_count']
            favorites += stats['favorite_count']

            total_reactions += stats['reaction_count']
            total_retweets += stats['retweet_count']
            total_favorites += stats['favorite_count']

        print(f"Number of source tweets   : {source_tweets}")    
        print(f"Number of reactions       : {reactions}")    
        print(f"Number of retweets        : {retweets}")
        print(f"Number of favorites       : {favorites}") 

        # Calculate averages
        avg_reactions = avg_comp_and_print(reactions, source_tweets, "reactions")
        avg_retweets = avg_comp_and_print(retweets, source_tweets, "retweets")
        avg_favorites = avg_comp_and_print(favorites, source_tweets, "favorites")
        print("\n") 

    print(f"Total number of source tweets   : {total_source_tweets}")    
    print(f"Total number of reactions       : {total_reactions}")    
    print(f"Total number of retweets        : {total_retweets}")
    print(f"Total number of favorites       : {total_favorites}")        

    # Calculate averages
    avg_reactions = avg_comp_and_print(total_reactions, total_source_tweets, "all reactions")
    avg_retweets = avg_comp_and_print(total_retweets, total_source_tweets, "all retweets")
    avg_favorites = avg_comp_and_print(total_favorites, total_source_tweets, "all favorites")
    print("\n\n")