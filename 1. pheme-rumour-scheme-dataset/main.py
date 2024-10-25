import os
import csv
import json
import operator
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from joy_centralities_unweighted import all_centralities

charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'
ottawa = 'ottawashooting'

# Pick a folder
FOLDER = charlie

# Get the current working directory
current_directory = os.getcwd()

# Un Directed Graph for tweet network
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
# This function is from Bachelor Thesis of Joy Kwant
def position_to_csv(pos, graph_name):
    """ Exports dictionary of positions of node, created by NetworkX spring_layout.
    @param pos: position disctionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open('csv\pos_dic_'+ graph_name + '.csv', 'w') as f:
        for key in pos.keys():
            f.write("%s,%s,%s\n"%(key, pos[key][0], pos[key][1]))

# Import
# This function is from Bachelor Thesis of Joy Kwant
def csv_dict_position(pos, graph_name):
    """ Imports the position dictionary, for each node there is a x,y-coordinate.
    @param pos: empty position dictionary.
    @param graph_name: name of graph (tweet or following) with folder name.
    """
    with open('csv\pos_dic_'+ graph_name + '.csv', newline='') as csvfile:
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
                    
    # print("Number of Nodes:", len(list(G.nodes)))
    #print("Number of Edges:", len(list(G.edges)))            


    # plot_graph(G, network)
    # plt.show()




# LINK ANALYSIS, project instruction #3

# This function is from the Bachelor Thesis of Joy Kwant
def hits(G, graph_name):
    """ Perform the HITS algorithm on graph G, but first converts undirected graph to directed graph,
    and stores the outcome of the Hubs and Authorities in descending order in csv files.
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G. 
    """ 
    print("in hits")
    if not G.is_directed():
        H = G.to_directed()                                                                     # Converts undirected graph to a directed graph.
    else:
        H = G.copy()

    h, a = nx.hits(H)                                                                           # Returns two dictionaries of Hubs and Authorities.

    print("sorted")
    h = sorted(h.items(), key = operator.itemgetter(1), reverse = True)
    a = sorted(a.items(), key = operator.itemgetter(1), reverse = True)


    with open('csv\hits_hubs_' + graph_name + '.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in h))

    with open('csv\hits_authorities_' + graph_name + '.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in a))

    # Find the intersection between the user IDs with the top 10 hub and authority scores
    match = set(h_id[0] for h_id in h[:10]) & set(a_id[0] for a_id in a[:10])
    print(f"we found {len(match)} matches between top 10s: {match}")

    return h[:10], a[:10]


# This function is from the Bachelor Thesis of Joy Kwant
def cluster_coefficient(G, graph_name):
    """ Perfoms the cluster coefficient on graph G and stores the outcome in descending order 
    and as dictionary in csv files.
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G. 
    """ 
    cc = nx.clustering(G)

    # with open(f'dict_clustercoeff_{graph_name}.csv', 'w') as f:
    #     for key in cc_weigth.keys():
    #         f.write("%s,%s\n"%(key,cc_weigth[key])) 

    cc = sorted(cc.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open(f'csv\clustercoeff_{graph_name}_desc.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in cc))

    top_ten_cc = cc[:10]
    print("Top ten cluster coefficients are \n", top_ten_cc)

    return top_ten_cc      


# This function is from the Bachelor Thesis of Joy Kwant
def undirected_connected_components(G):
    """ Prints the list of connected components of an undirected network.
    @param G: The NetworkX graph.
    """
    cc = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    print("Graph has "+ str(len(cc)) + " connected components:")
    cc_largest = cc[0] if cc else 0
    print(cc)
    return cc, cc_largest

def directed_connected_components(G):
    """ Prints the list of connected components of an directed network.
    @param G: The NetworkX graph.
    """
    strong_cc = [len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
    weak_cc = [len(c) for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True)]
    print("Graph has "+ str(len(strong_cc)) + " strongly connected components")
    print("Graph has "+ str(len(weak_cc)) + " weakly connected components")
    print(strong_cc)

    # Sizes of each strongly connected component
    scc_largest = strong_cc[0] if strong_cc else 0
    wcc_largest = weak_cc[0] if weak_cc else 0

    print("Sizes of each Strongly Connected Component:", scc_largest)
    print("Sizes of each Weakly Connected Component:", wcc_largest)

    return strong_cc, weak_cc, scc_largest, wcc_largest


def compute_diameter(G):
    # Calculate all pairs shortest paths
    lengths = dict(nx.all_pairs_shortest_path_length(G))

    # Find the diameter
    diameter = 0

    # Iterate through lengths to find the maximum
    for source, target_lengths in lengths.items():
        for target, path_length in target_lengths.items():
            if path_length != float('inf'):  # Only consider reachable nodes
                diameter = max(diameter, path_length)

    print("Network Diameter of the Directed Graph:", diameter)

    return diameter


def degree_distribution(G, G_name):

    # Calculate in-degree and out-degree for each node
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())

    # Convert degrees to lists
    in_degree_values = list(in_degrees.values())
    out_degree_values = list(out_degrees.values())

    # Calculate minimum, maximum, average, and median for in-degrees
    in_degree_min = min(in_degree_values)
    write_to_csv_file("Minimum in-degree", in_degree_min, G_name)
    in_degree_max = max(in_degree_values)
    write_to_csv_file("Maximum in-degree", in_degree_max, G_name)
    in_degree_avg = np.mean(in_degree_values)
    write_to_csv_file("Average in-degree", in_degree_avg, G_name)
    in_degree_median = np.median(in_degree_values)
    write_to_csv_file("Median in-degree", in_degree_median, G_name)

    # Calculate minimum, maximum, average, and median for out-degrees
    out_degree_min = min(out_degree_values)
    write_to_csv_file("Minimum out-degree", out_degree_min, G_name)
    out_degree_max = max(out_degree_values)
    write_to_csv_file("Maximum out-degree", out_degree_max, G_name)
    out_degree_avg = np.mean(out_degree_values)
    write_to_csv_file("Average out-degree", out_degree_avg, G_name)
    out_degree_median = np.median(out_degree_values)
    write_to_csv_file("Median out-degree", out_degree_median, G_name)


    # Print results
    print("In-Degree Centrality Distribution:")
    print(f"Minimum: {in_degree_min}, Maximum: {in_degree_max}, Average: {in_degree_avg:.2f}, Median: {in_degree_median}")

    print("\nOut-Degree Centrality Distribution:")
    print(f"Minimum: {out_degree_min}, Maximum: {out_degree_max}, Average: {out_degree_avg:.2f}, Median: {out_degree_median}")


# Save the results to a CSV file
def write_to_csv_file(metric_name, metric_result, graph_name):
    
    with open(f'csv\metrics_report_{graph_name}.csv','a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([metric_name, metric_result])



# METRICS, project instruction #1
def metric_report(G, G_name):
    """ Calculate the following metrics: number of vertices, number of edges,
    degree distribution, centrality indices, clustering coefficient,
    network diameter, density, number of connected components and, size of
    the connected components.
    Save the results of the metrics to a csv/txt file.  # TODO: update file format
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G (AA, DA, ..).
    """
    # Number of nodes and edges of G
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()
    print(f"Number of nodes in {G_name}: {n_nodes}")
    print(f"Number of edges in {G_name}: {n_edges}")
    write_to_csv_file("Number of nodes", n_nodes, G_name)
    write_to_csv_file("Number of edges", n_edges, G_name)

    # Degree centrality/distribution (in-degree and out-degree)
    # Minimum, Maximum, Average, Median (middle number)
    degree_distribution(G, G_name)

    # Centrality indices (node with highest degree)
    # 1. Degree,  2. Betweenness,  3. Closeness and 4. Eigenvector
    top_ten_degree, top_ten_betweenness, top_ten_closeness, top_ten_eigenvector = all_centralities(G, G_name)
    write_to_csv_file("Top ten degree", top_ten_degree, G_name)
    write_to_csv_file("Top ten betweenness", top_ten_betweenness, G_name)
    write_to_csv_file("Top ten closeness", top_ten_closeness, G_name)
    write_to_csv_file("Top ten eigenvector", top_ten_eigenvector, G_name)

    # Clustering coefficient
    top_ten_ccoeff = cluster_coefficient(G, G_name)
    write_to_csv_file("Top ten cluster coefficients", top_ten_ccoeff, G_name)
    
    # Network diameter
    # Returns the diameter of the graph G.
    diameter = compute_diameter(G)
    write_to_csv_file("Diameter", diameter, G_name)

    # Graph density
    graph_density = nx.density(G)
    write_to_csv_file("Density", diameter, G_name)
    print(f"The graph density is: {graph_density}")

    top_ten_h, top_ten_a = hits(G, G_name)
    write_to_csv_file("Top ten hits", top_ten_h, G_name)
    write_to_csv_file("Top ten authorities", top_ten_a, G_name)

    # Number and size of connected components
    if not G.is_directed():
        # Undirected graph
        con_comp, cc_largest = undirected_connected_components(G)
        write_to_csv_file("The number of the connected components", con_comp, G_name)
        write_to_csv_file("The size of the largest connected component", cc_largest, G_name)
    else:
        # Directed graph: get strongly and weakly connected components
        strong_con_comp, weak_con_comp, scc_largest, wcc_largest = directed_connected_components(G)
        write_to_csv_file("The number of strongly connected components", strong_con_comp, G_name)
        write_to_csv_file("The number of weakly connected components", weak_con_comp, G_name)
        write_to_csv_file("The size of the largest strongly connected component", scc_largest, G_name)
        write_to_csv_file("The size of the largest weakly connected component", wcc_largest, G_name)

##### MAIN


# creation_of_network(T, "tweets")
creation_of_network(F, "following")

# hits(T, FOLDER + "_" + "tweets")
# hits(F, FOLDER + "_" + "following")

metric_report(F, FOLDER + "_" + "following")


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