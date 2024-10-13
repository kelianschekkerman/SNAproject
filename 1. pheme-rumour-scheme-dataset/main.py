import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

FOLDER = putin




# Get the current working directory
current_directory = os.getcwd()

# Create new empty global graph G (Un Directed Graph)
G = nx.Graph()




def place_edge(G, first_node, second_node):
    """ Places an edges between two nodes in graph G. Initialzie the weight attribute with start weight 1
    or increases the weight of the edge attribute if the edge already exists.
    @param G: The NetworkX graph.
    @param first_node: Node 1 of the two nodes, where an edge should be placed.
    @param second_node: Node 2 of the two nodes, where an edge should be placed.
    """ 
    if G.has_edge(first_node, second_node):                                                 # First collaboration.
        G[first_node][second_node]['weight'] += 1
    else:
        G.add_edge(first_node, second_node, weight = 1)


def place_nodes_in_graph(G, parent, tweet_id):
    # Add nodes
    if parent not in G:
        G.add_node(parent, color = 'purple')
    G.add_node(tweet_id, color = 'purple')

    # Place edge
    place_edge(G, parent, tweet_id)


# Function to recursively traverse the tweet thread and generate connections
def create_connections(G, thread, parent = None):
    for tweet_id, replies in thread.items():
        if parent:
            print(f"Connection: {parent} -> {tweet_id}")
            place_nodes_in_graph(G, parent, tweet_id)

        else: # source tweet
            G.add_node(tweet_id, color = 'red')

            
        # If there are nested replies, recursively process them
        if isinstance(replies, dict) and replies:
            create_connections(G, replies, tweet_id)




def plot_graph_tweets(G):
    fig, ax = plt.subplots(figsize=(12, 7))

    pos = nx.spring_layout(G, k=0.155, seed=3968461)
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
    source_patch = mpatches.Patch(color='red', label='Source Tweet')
    reply_patch = mpatches.Patch(color='purple', label='Reply Tweet')
    plt.legend(handles=[source_patch, reply_patch])

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    ax.set_title(f"Folder: {FOLDER}, network of tweets", font)
    # Change font color for legend
    font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")

    plt.show()




def network_of_tweets():

    # Walk through the directory
    for root, dirs, files in os.walk(current_directory):
        #print('root: ', root)
        #print('dirs: ',dirs) 

        # if 'threads' not in root:
        #     for file in files:
        #         # Full file path
        #         file_path = os.path.join(root, file)
        #         print(file_path)

        if FOLDER in root:
            
            for file in files:
                # Full file path
                file_path = os.path.join(root, file)
                # if "structure.json" in file_path:
                #     print(file_path)
                if file == "structure.json":
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Print the data
                    print(data)
                    create_connections(G, data)

                    # print("Number of Nodes:", len(list(G.nodes)))
                    #print("Nodes:", list(G.nodes))
                    # print("Number of Edges:", len(list(G.edges)))            
                    #print("Edges:", list(G.edges))  
                    

    print("Number of Nodes:", len(list(G.nodes)))
    # print("Nodes:", list(G.nodes))
    print("Number of Edges:", len(list(G.edges)))            
    # print("Edges:", list(G.edges)) 


    plot_graph_tweets(G)




##### MAIN





network_of_tweets()




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