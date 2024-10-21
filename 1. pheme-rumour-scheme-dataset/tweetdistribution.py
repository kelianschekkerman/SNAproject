import os
import csv
import pytz
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from collections import defaultdict
#from get_timezones import timezone_map  # Timezone map to match strings to pytz timezones

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

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

# Pick a folder
FOLDER = charlie

current_directory = os.getcwd()

# Target timezone (Amsterdam)
amsterdam_tz = pytz.timezone('Europe/Amsterdam')


# Network of tweets
T = nx.Graph()
Tw = nx.Graph()



def get_timestamp(folder):
    """
    Function to process files inside a given folder.
    """
    for root, dirs, files in os.walk(folder):
        
        if "source-tweet" in root:
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    id = data["id_str"]
                    
                    created_at = data["created_at"]
                    user_data = data.get('user', {})  # Get 'user' data, or an empty dict if it doesn't exist
                    time_zone = user_data.get('time_zone', 'NaN')
                    # print(f"{id} : {created_at}, {time_zone}") 

                    ## Converting
                    #amsterdam_time = convert_to_amsterdam(created_at, time_zone)
                    utc_time = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    
                    #print(f"ID: {id}, Amsterdam Time: {utc_time}\n")
                    # print(f"ID: {id}, UTC +0: {utc_time}\n")

                    return utc_time



def add_reaction_tweet(G, parent, tweet_id, t_stamp):
   
    G.add_node(tweet_id, color = 'black', timestamp = t_stamp)

    # Place edge
    G.add_edge(parent, tweet_id)





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
def position_to_csv(pos, graph_name):
    """ Exports dictionary of positions of node, created by NetworkX spring_layout.
    @param pos: position disctionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open('pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))


# Import
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

    # Return None if no source tweet was found (in case something went wrong)
    return None, None


def add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter):    
    #print(tweet.tweet_id)

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



def add_tweet_to_network(G, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iter):
    # Add the tweet to the graph
    if tweet.type == "source":
        print("source tweet")
        add_source_tweet(G, source_tweet=tweet.tweet_id, t_stamp=tweet.timestamp, misinfo=tweet.misinformation, true=tweet.true)
    else:   # reply tweet
        print("reaction")
        add_reaction_tweet(G, parent=tweet.reply_to, tweet_id=tweet.tweet_id, t_stamp=tweet.timestamp)
        add_replies_to_dictionary(misinfo_dict, true_dict, uncertain_dict, tweets_dict, tweet, current_iter)

            




def plot_graph(G, network):
    print("create plot\n")
    fig, ax = plt.subplots(figsize=(12, 7))

    nodes_tweet_network = {} 
    csv_dict_position(nodes_tweet_network, FOLDER + "_" + network)

    nodes_to_remove = []
    # print(G.number_of_nodes())
    # print(len(nodes_tweet_network.keys())) 
    for n in G.nodes():
        if n not in nodes_tweet_network.keys():
            #print(n)
            nodes_to_remove.append(n)
    # print(f"count {len(nodes_to_remove)}")


    # # print("MISSING:")
    # # for n in nodes_tweet_network.keys():
    # #     if n not in G.nodes():
    # #         print(n)
    # # print("\n")


    G.remove_nodes_from(nodes_to_remove)   
    
    # print(f" Nodes in the graph:  {G.number_of_nodes()} ")
    # print(len(nodes_tweet_network.keys())) 
    
    #pos = nx.spring_layout(G, k=0.155, seed=3968461)
    # position_to_csv(pos, FOLDER + "_" + network)

    pos = {} 
    csv_dict_position(pos, FOLDER + "_" + network)

    node_color = [G.nodes[n]['color'] for n in G.nodes]


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


##### MAIN


# First loop for getting first and last timestamp of event
first_timestamp = None

# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    
    if FOLDER in root:
        first_folder = os.path.join(root, dirs[0])  # First folder
        last_folder = os.path.join(root, dirs[-1])  # Last folder TODO: remove this line?
        # print(f"First Folder: {first_folder}")
        # print(f"Last Folder: {last_folder}")

        first_timestamp = get_timestamp(first_folder)

        break

last_timestamp = first_timestamp

# Second loop

tweets = []

is_misinfo = None
is_true = None
# Walk through the directory
for root, dirs, files in os.walk(current_directory):
    if FOLDER in root:        
        # Loop first goes through seperate files
        for file in files:
            # Full file path
            file_path = os.path.join(root, file)

            if "annotation.json" in file_path:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    is_misinfo = data['misinformation']
                    # print(f"misformation: {is_misinfo}")
                    if 'true' in data:
                        is_true = data['true']
                        # print(f"true: {is_true}")

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
                    # print(f"{id} : {created_at}, {time_zone}") 

                    ## Converting
                    #timestamp_ams = convert_to_amsterdam(created_at, time_zone)
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")

                    # print(f"ID: {id}, Amsterdam Time: {timestamp_ams}\n")

                    # Add tweet to the list of tweets
                    tweets.append(Tweet(tweet_id=id, type="reply", timestamp=time_stamp_utc0, reply_to=parent))
                    add_reaction_tweet(T, parent, id, time_stamp_utc0)
                    
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
                    time_zone = user_data.get('time_zone', 'NaN')
                    # print(f"{id} : {created_at}, {time_zone}") 

                    ## Converting
                    #timestamp_ams = convert_to_amsterdam(created_at, time_zone)
                    time_stamp_utc0 = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    

                    # print(f"ID: {id}, Amsterdam Time: {timestamp_ams}\n")
                    # print(f"Misformation: {is_misinfo} and true: {is_true}\n")

                    # Add tweet to the list of tweets
                    tweets.append(Tweet(tweet_id=id, type="source", timestamp=time_stamp_utc0, misinformation=is_misinfo, true=is_true))
                    add_source_tweet(T, id, time_stamp_utc0, is_misinfo, is_true)

                    # Reset the info for next thread folder
                    is_misinfo = None
                    is_true = None

                    # Check if this tweet is later than the currently found last tweet
                    if time_stamp_utc0 > last_timestamp:
                        last_timestamp = time_stamp_utc0

# print(f"len of tweets list {len(tweets)}")
# print(f"graph T list {T.number_of_nodes()}")

# ###########################################################################################################################
# Sort tweets on timestamp
tweets.sort(key=lambda tweet: tweet.timestamp)
# for tweet in tweets:
#     print(tweet)


# Dictionary for the barplots
tweets_dict = {tweet.tweet_id: tweet for tweet in tweets}


# # Based on the timestamps of the first and last tweet, determine the iteration duration
max_iter = 5
iteration_duration = (last_timestamp - first_timestamp)/max_iter

# print(f"FIRST TIMESTAMP = {first_timestamp}")
# print(f"ITERATION DURATION = {iteration_duration}")
# print(f"LAST TIMESTAMP = {last_timestamp}")

# lower = first_timestamp
# upper = first_timestamp + iteration_duration
# print(f"FIRST ITERATION, BOUNDARY = [{lower}, {upper}]")


misinfo_dict = defaultdict(list)
true_dict = defaultdict(list)
uncertain_dict = defaultdict(list)

current_iteration = 1   # Start at iteration 1
# Keep track of iterations
for tweet in tweets:
    # print(tweet)
    # print((current_iteration * iteration_duration) + first_timestamp)
    # if tweet.timestamp == last_timestamp:
    #     print(f"\n THIS IS THE LAST TWEET = {last_timestamp}")
    #     print(tweet.timestamp)
    #     print((current_iteration * iteration_duration) + first_timestamp)

    # First check if the tweet is outside of the current iteration window, plot the graph and increase iteration
    if tweet.timestamp > ((current_iteration * iteration_duration) + first_timestamp):
        # Plot
        plot_graph(Tw, "tweets")
        #plt.show()
        # lower = (current_iteration * iteration_duration) + first_timestamp
        current_iteration += 1
        # upper = (current_iteration * iteration_duration) + first_timestamp
        # print(f"NEW ITERATION CASE >, NEW BOUNDARY = [{lower}, {upper}]")
    
    # Then decide what to do with the tweet
    # If this tweet is on the upper boundary of the iteration, add the tweet to the iteration first, then plot
    if tweet.timestamp == ((current_iteration * iteration_duration) + first_timestamp):
        # Add tweet (== so still belongs to the current iteration)
        print(current_iteration)
        add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)
        # Then plot
        plot_graph(Tw, "tweets")
        #plt.show()
        # lower = (current_iteration * iteration_duration) + first_timestamp
        current_iteration += 1
        # upper = (current_iteration * iteration_duration) + first_timestamp
        # print(f"NEW ITERATION CASE ==, NEW BOUNDARY = [{lower}, {upper}]")
    else :      # Tweet belongs in current iteration, add tweet then continue on to the next tweet
        # Add tweet to current iteration
        print(current_iteration)
        add_tweet_to_network(Tw, tweet, misinfo_dict, true_dict, uncertain_dict, tweets_dict, current_iteration)


# Dictionaries for barplots
print(f"current iter : {current_iteration}\n")

print(f"misinfo dict {misinfo_dict}")
for k in misinfo_dict.keys():
    print(f"iteration {k} : {len(misinfo_dict[k])}")

print(f"\ntrue dict {true_dict}")
for k in true_dict.keys():
    print(f"iteration {k} : {len(true_dict[k])}")

print(f"\nuncertain dict {uncertain_dict}")
for k in uncertain_dict.keys():
    print(f"iteration {k} : {len(uncertain_dict[k])}")


# #plot_graph(T, "tweets")
# plot_graph(Tw, "tweets")        ## !!!! Bij deze wordt alles geplot

#plt.show()


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