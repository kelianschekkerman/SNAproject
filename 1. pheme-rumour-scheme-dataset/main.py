import os
import csv
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

from metrics import metric_report
from community_metrics import community_metric_report, remove_noise, plot_community_graph

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'
ottawa = 'ottawashooting'

REMOVE_NOISE = True

COLOR_SOURCE_TWEET = "red"
COLOR_REPLY_TWEET = "green"
COLOR_RETWEET_TWEET = "blue"

# Pick a folder
FOLDER = putin

# Get the current working directory
current_directory = os.getcwd()

# Un Directed Graph for tweet network
T = nx.Graph()

# Directed graph for following network
F = nx.DiGraph()



def add_tweet(G, parent, tweet_id):
    # Add nodes
    if parent not in G:
        G.add_node(parent, color = COLOR_REPLY_TWEET)
    G.add_node(tweet_id, color = COLOR_REPLY_TWEET)

    # Place edge
    G.add_edge(parent, tweet_id)
    


# Function to recursively traverse the tweet thread and generate connections
def tweet_connections(G, thread, parent = None):
    for tweet_id, replies in thread.items():
        if parent:
            print(f"Connection: {parent} -> {tweet_id}")
            add_tweet(G, parent, tweet_id)
        else:                                                                               # Source tweet
            G.add_node(tweet_id, color = COLOR_SOURCE_TWEET)

            
        # If there are nested replies, recursively process them
        if isinstance(replies, dict) and replies:
            tweet_connections(G, replies, tweet_id)


def add_follower(G, follower, followed):


    # Place edge
    G.add_edge(follower, followed)


# Export
# This function is from Bachelor Thesis of Joy Kwant
def position_to_csv(pos, graph_name):
    """ Exports dictionary of positions of node, created by NetworkX spring_layout.
    @param pos: position disctionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open(r'csv\pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))

# Import
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




def plot_graph(G, network):
    fig, ax = plt.subplots(figsize=(12, 7))

    # Remove retweet user nodes that do not have 'followers' attribute
    #nodes_to_remove = [n for n, attr in G.nodes(data=True) if 'followers' not in attr]
    #G.remove_nodes_from(nodes_to_remove)

    pos = nx.spring_layout(G, k=0.155, seed=3968461)
    position_to_csv(pos, FOLDER + "_" + network)
    # pos = {} 
    # csv_dict_position(pos, FOLDER + "_" + network)

    node_color = [G.nodes[n]['color'] for n in G.nodes]

    node_sizes = []
    standard_size = 20
    if network == 'tweets':
        node_sizes =  [ G.nodes[n]['retweets'] + standard_size for n in G.nodes]
    elif network == "following":
        #node_sizes =  [standard_size for n in G.nodes]   
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

    # plt.show()


def creation_of_network(G, network):

    # Walk through the directory
    for root, dirs, files in os.walk(current_directory):
        if FOLDER in root:
            
            for file in files:
                # Full file path
                file_path = os.path.join(root, file)
                if network == "tweets" and file == "structure.json":
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    tweet_connections(G, data)

                if network == "following" and file == "retweets.json":
                    # Add users from retweets to follower network
                    with open(file_path, 'r') as file:
                        data = [json.loads(line) for line in file]
                    for tweet in data:
                        #data = json.loads(line)
                        user_id = str(tweet['user']['id'])
                        time_zone = tweet['user']['time_zone']
                        followers_count = tweet['user']['followers_count']
                        #print(f"{user_id} with follower count {followers_count} and timezone {time_zone}")
                        if user_id not in G:
                            G.add_node(user_id, color=COLOR_RETWEET_TWEET, followers = followers_count, time_zone = time_zone)
                
                if network == "following" and "who-follows" in file_path:
                    with open(file_path, 'r') as file:
                        for line in file:
                            # Split each line by the tab character to get follower and followed
                            follower, followed = line.strip().split('\t')
                            # Add the follower relationship to the graph
                            add_follower(G, follower, followed)

                if "source-tweet" in root:
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            if network == "tweets":
                                id = data["id_str"]    
                                retweet_count = data["retweet_count"]
                                name = data['user']['name'] 
                                print(name)
                                G.add_node(id, name = name, color = COLOR_SOURCE_TWEET, retweets = retweet_count)
                            elif network == "following":
                                user_id = str(data['user']['id'])
                                time_zone = data['user']['time_zone']
                                followers_count = data['user']['followers_count']
                                name = data['user']['name']
                                #print(f"{user_id} and follow count {followers_count}, name ={ name}")
                                G.add_node(user_id, name = name,  color = COLOR_SOURCE_TWEET, followers = followers_count, time_zone=time_zone)


                if "reaction" in root:
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            if network == "tweets":
                                id = data["id_str"] # Tweet ID
                                retweet_count = data["retweet_count"]  
                                G.add_node(id, color = COLOR_REPLY_TWEET, retweets = retweet_count)
                            elif network == "following":
                                user_id = str(data['user']['id'])
                                time_zone = data['user']['time_zone']
                                followers_count = data['user']['followers_count']
                                #print(f"{user_id} and follow count {followers_count}")
                                G.add_node(user_id, color = COLOR_REPLY_TWEET, followers = followers_count, time_zone=time_zone)   

    print("Number of Nodes:", len(list(G.nodes)))
    print("Number of Edges:", len(list(G.edges)))            

    if REMOVE_NOISE:
        remove_noise(G)
        print("Number of Nodes:", len(list(G.nodes)))
        print("Number of Edges:", len(list(G.edges)))  

    plot_graph(G, network)

    #plt.show()

##### MAIN

creation_of_network(T, "tweets")
#creation_of_network(F, "following")
plt.show()

#metric_report(T, FOLDER + "_" + "tweets")
#metric_report(F, FOLDER + "_" + "following")

#community_metric_report(F, FOLDER + "_" + "following")



#plot_community_graph(F, FOLDER, "following", 'Louvain')

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