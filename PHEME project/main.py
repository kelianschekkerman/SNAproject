import os
import csv
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

from metrics import metric_report
from community_metrics import community_metric_report, remove_noise, plot_community_graph

# The different breaking news events
charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'
ottawa = 'ottawashooting'

# Pick a folder
FOLDER = german_airplane

# CHoose to remove isolated nodes in the graph
REMOVE_NOISE = False


# Color setting for the different type of tweets
COLOR_SOURCE_TWEET = "red"
COLOR_REPLY_TWEET = "green"
COLOR_RETWEET_TWEET = "blue"


# For calling functions
CREATION_TWEETS_NETWORK = False
CREATION_FOLLOWING_NETWORK = True
METRICS_REPORT = False
COMMUNITY_REPORT = False
PLOT_COMMUNITIES = True


# Get the current working directory
current_directory = os.getcwd()

# UnDirected Graph for tweet network
T = nx.Graph()

# Directed graph for following network
F = nx.DiGraph()




def add_tweet(G, parent, tweet_id):
    """
    Adds a reaction tweet and the tweet it reacted to (parent) to the graph.
    
    @param G: The NetworkX graph.
    @param parent: The tweet to which the reacted tweet responded.
    @param tweet_id: The ID of the reaction tweet.
    """
    # Check if the parent tweet node exists
    if parent not in G:
        G.add_node(parent, color = COLOR_REPLY_TWEET)
    G.add_node(tweet_id, color = COLOR_REPLY_TWEET)

    # Place edge
    G.add_edge(parent, tweet_id)
    

def tweet_connections(G, thread, parent = None):
    """
    Recursively traverses a tweet thread to create connections between parent and reply tweets.
    
    @param G: The NetworkX graph.
    @param thread: A dictionary representing the tweet thread, where each key is a tweet ID 
                   and each value is a dictionary of replies (nested in the same format).
    @param parent: The ID of the tweet being replied to in the current context. Defaults to None, 
                   meaning the tweet is the source tweet in the thread.
    """
    # Iterate over each tweet in the thread dictionary
    for tweet_id, replies in thread.items():
        if parent:
            add_tweet(G, parent, tweet_id)
        else: 
            # If no parent, this tweet is the source tweet, so add it with a unique color attribute
            G.add_node(tweet_id, color = COLOR_SOURCE_TWEET)

        # If there are nested replies, recursively process them
        if isinstance(replies, dict) and replies:
            tweet_connections(G, replies, tweet_id)


# This function is from Bachelor Thesis of Joy Kwant
def position_to_csv(pos, graph_name):
    """ 
    Exports dictionary of positions of node, created by NetworkX spring_layout.
    
    @param pos: position disctionary.
    @param graph_name: Name of graph (tweet or following) with folder name.
    """
    with open(r'csv\pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))


# This function is from Bachelor Thesis of Joy Kwant
def csv_dict_position(pos, graph_name):
    """ 
    Imports the position dictionary, for each node there is a x,y-coordinate.
    
    @param pos: empty position dictionary.
    @param graph_name: Name of graph (tweet or following) with folder name.
    """
    with open(r'csv\pos_dic_'+ graph_name + '.csv', newline='') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            pos.setdefault(row[0])
            pos[row[0]] = [float(row[1]), float(row[2])]               



def plot_graph(G, network):
    """ 
    Plot the graph using NetworkX.
    
    @param G: the NetworkX grpah.
    @param network: The network type. ("tweets" or "following").
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Compute postions of the node and export the dictionary to a csv file
    pos = nx.spring_layout(G, k=0.155, seed=3968461)
    position_to_csv(pos, FOLDER + "_" + network)
    
    # Retrieve postions from csv file (import) 
    # pos = {} 
    # csv_dict_position(pos, FOLDER + "_" + network)

    node_color = [G.nodes[n]['color'] for n in G.nodes]

    node_sizes = []
    standard_size = 20
    if network == 'tweets':
        node_sizes =  [ G.nodes[n]['retweets'] + standard_size for n in G.nodes]
    elif network == "following":
        #node_sizes =  [standard_size for n in G.nodes]   # This is for smaller network (e.g. putin)
        node_sizes =  [(G.nodes[n]['followers']/1000) + standard_size for n in G.nodes]   

    nx.draw_networkx(
            G,
            pos = pos,
            with_labels = False,
            node_color = node_color,
            node_size = node_sizes,
            edge_color = "gainsboro",
            alpha = 0.4,
        )
    
    # Different legends for the different networks
    if network == "tweets":
        # Create a legend using mpatches for the source and reply colors
        source_patch = mpatches.Patch(color=COLOR_SOURCE_TWEET, label='Source Tweet')
        reply_patch = mpatches.Patch(color=COLOR_REPLY_TWEET, label='Reply Tweet')
        plt.legend(handles=[source_patch, reply_patch])
    else:
        user_source_patch = mpatches.Patch(color=COLOR_SOURCE_TWEET, label='User of Source tweet')
        user_reply_patch = mpatches.Patch(color=COLOR_REPLY_TWEET, label='User of a Reply')
        user_retweet_patch = mpatches.Patch(color=COLOR_RETWEET_TWEET, label='User of a Retweet')
        plt.legend(handles=[user_source_patch, user_reply_patch,user_retweet_patch])

    # Add node labels only for nodes that have the 'name' attribute
    labels = {node: attr['name'] for node, attr in G.nodes(data=True) if 'name' in attr}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    if network == "tweets":
        ax.set_title(f"Folder: {FOLDER}, network of tweets, node size represents the number of retweets", font)
    else:
        ax.set_title(f"Folder: {FOLDER}, network of following, node size represents the number of followers", font)
    
    # Change font color for legend
    font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")



def creation_of_network(G, network):
    """ 
    COnstructs the graph using the data from the chosen folder.
    
    @param G: the NetworkX grpah.
    @param network: The type of network to construct. ("tweets" or "following").
    """
    # Walk through the directory
    for root, dirs, files in os.walk(current_directory):
        # Check if the current directory is for the specific news event (FOLDER)
        if FOLDER in root:  
            for file in files:
                # Full file path
                file_path = os.path.join(root, file)
                
                # If constructing a "tweets" network, we fetch the nested reaction structure from "structure.json"
                if network == "tweets" and file == "structure.json":
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    tweet_connections(G, data)

                # If constructing a "following" network, we retrieve the information about the users retweeting the source tweet
                if network == "following" and file == "retweets.json":
                    # Add users from retweets to follower network
                    with open(file_path, 'r') as file:
                        data = [json.loads(line) for line in file]
                    for tweet in data:
                        user_id = str(tweet['user']['id'])
                        time_zone = tweet['user']['time_zone']
                        followers_count = tweet['user']['followers_count']

                        # Add user node if it doesn't already exist
                        if user_id not in G:
                            G.add_node(user_id, color=COLOR_RETWEET_TWEET, followers = followers_count, time_zone = time_zone)
                
                # If constructing a "following" network, we fetch the following data from the "who-follows-who.dat"
                if network == "following" and "who-follows" in file_path:
                    with open(file_path, 'r') as file:
                        for line in file:
                            # Split each line by the tab character to get follower and followed
                            follower, followed = line.strip().split('\t')
                            # Place an edge between follower and followed
                            G.add_edge(follower, followed)

                # If the directory is the "source-tweet" folder
                if "source-tweet" in root:
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            
                            # Add node for the source tweet or the user based on network type
                            if network == "tweets":
                                id = data["id_str"]    
                                retweet_count = data["retweet_count"]
                                name = data['user']['name'] 
                                G.add_node(id, name = name, color = COLOR_SOURCE_TWEET, retweets = retweet_count)
                            elif network == "following":
                                user_id = str(data['user']['id'])
                                time_zone = data['user']['time_zone']
                                followers_count = data['user']['followers_count']
                                name = data['user']['name']
                                G.add_node(user_id, name = name,  color = COLOR_SOURCE_TWEET, followers = followers_count, time_zone=time_zone)

                # If the directory is the "reactions" folder
                if "reaction" in root:
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            
                            # Add node for each reaction tweet or the user based on network type
                            if network == "tweets":
                                id = data["id_str"] # Tweet ID
                                retweet_count = data["retweet_count"]  
                                G.add_node(id, color = COLOR_REPLY_TWEET, retweets = retweet_count)
                            elif network == "following":
                                user_id = str(data['user']['id'])
                                time_zone = data['user']['time_zone']
                                followers_count = data['user']['followers_count']
                                G.add_node(user_id, color = COLOR_REPLY_TWEET, followers = followers_count, time_zone=time_zone)   

    # Print the current number of nodes and edges in the graph
    print("Number of Nodes:", len(list(G.nodes)))
    print("Number of Edges:", len(list(G.edges)))            

    if REMOVE_NOISE:
        remove_noise(G)
        print("Number of Nodes:", len(list(G.nodes)))
        print("Number of Edges:", len(list(G.edges))) 





##### MAIN


if CREATION_TWEETS_NETWORK:
    creation_of_network(T, "tweets")
    #plot_graph(T, "tweets")


if CREATION_FOLLOWING_NETWORK:
    creation_of_network(F, "following")
    #plot_graph(F, "following")



if METRICS_REPORT and CREATION_TWEETS_NETWORK:
    metric_report(T, FOLDER + "_" + "tweets")


if METRICS_REPORT and CREATION_FOLLOWING_NETWORK:
    metric_report(F, FOLDER + "_" + "following")



if COMMUNITY_REPORT and CREATION_FOLLOWING_NETWORK:            # Only for the following network
    community_metric_report(F, FOLDER + "_" + "following")    



if PLOT_COMMUNITIES and CREATION_FOLLOWING_NETWORK:            # Only for the following network
    # When plotting the communities the isolated node should be removed
    if not REMOVE_NOISE: # Check if the removing is already done
        remove_noise(F)
        print("Number of Nodes:", len(list(F.nodes)))
        print("Number of Edges:", len(list(F.edges))) 

    # Compute the new postions of the node and export the dictionary to a csv file
    pos = nx.spring_layout(F, k=0.155, seed=3968461)

    plot_community_graph(F, FOLDER, "following", pos, 'Louvain')
    
    if FOLDER == "putinmissing" or FOLDER == "germanwings-crash":
        plot_community_graph(F, FOLDER, "following", pos, 'Girvan Newman')


plt.show()





### Notes

# Structure.json
# {A: {B: {C,D}}, {E:{F}}, G, H}
# A -- B -- C,D
#   -- E -- F
#   -- G
#   -- H


# from annotation.json
# 'isrumour'        different colour in graph for rumour?
# mediatype?

# from <tweetid>.json from reaction folder and source tweet folder
# created_at


# retweet.json > for the source tweet


# Networks:
# - tweets
# - users