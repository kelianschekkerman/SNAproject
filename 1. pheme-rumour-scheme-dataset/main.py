import os
import csv
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

# Pick a folder
FOLDER = german_airplane




# Get the current working directory
current_directory = os.getcwd()

# Un Directed Graph for tweet netweork
T = nx.Graph()

# Directed graph for following network
F = nx.DiGraph()



def add_tweet(G, parent, tweet_id):
    # Add nodes
    if parent not in G:
        G.add_node(parent, color = 'purple')
    G.add_node(tweet_id, color = 'purple')

    # Place edge
    G.add_edge(parent, tweet_id)
    


# Function to recursively traverse the tweet thread and generate connections
def tweet_connections(G, thread, parent = None):
    for tweet_id, replies in thread.items():
        if parent:
            print(f"Connection: {parent} -> {tweet_id}")
            add_tweet(G, parent, tweet_id)
        else:                                                                               # Source tweet
            G.add_node(tweet_id, color = 'red')

            
        # If there are nested replies, recursively process them
        if isinstance(replies, dict) and replies:
            tweet_connections(G, replies, tweet_id)


def add_follower(G, follower, followed):
    # Add nodes
    G.add_node(follower, color = 'purple')
    G.add_node(followed, color = 'purple')

    # Place edge
    G.add_edge(follower, followed)





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




def plot_graph(G, network):
    fig, ax = plt.subplots(figsize=(12, 7))

    pos = nx.spring_layout(G, k=0.155, seed=3968461)
    position_to_csv(pos, FOLDER + "_" + network)
    # pos = {} 
    # csv_dict_position(pos, FOLDER + "_" + network)

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

    if network == "tweets":
        # Create a legend using mpatches for the source and reply colors
        source_patch = mpatches.Patch(color='red', label='Source Tweet')
        reply_patch = mpatches.Patch(color='purple', label='Reply Tweet')
        plt.legend(handles=[source_patch, reply_patch])
    else:
        user_patch = mpatches.Patch(color='purple', label='User')
        plt.legend(handles=[user_patch])


    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    ax.set_title(f"Folder: {FOLDER}, network of {network}", font)
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

                    # Print the data
                    #print(data)
                    tweet_connections(G, data)
                
                elif network == "following" and "who-follows" in file_path:
                    with open(file_path, 'r') as file:
                        for line in file:
                            # Split each line by the tab character to get follower and followed
                            follower, followed = line.strip().split('\t')

                            #print(f"{follower} --> {followed}")
                            
                            # Add the follower relationship to the graph
                            add_follower(G, follower, followed)


                        



                    
    print("Number of Nodes:", len(list(G.nodes)))
    #print("Number of Edges:", len(list(G.edges)))            

    
    plot_graph(G, network)
    plt.show()






##### MAIN


creation_of_network(T, "tweets")
#creation_of_network(F, "following")




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