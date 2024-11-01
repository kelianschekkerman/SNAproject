import csv
import ast
import numpy as np
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

from networkx.algorithms.community.centrality import girvan_newman


# For Clustering colors
colors = mcolors.CSS4_COLORS
html_colors = list(colors.values())[10:]
color_list = html_colors
del color_list[13:17]
colors2 = mcolors.XKCD_COLORS
html_colors2 = list(colors2.values())
color_list = color_list + html_colors2


# This function is from the Bachelor Thesis of Joy Kwant
def remove_noise(G):
    """ Removes nodes from graph with values, which have no connection 
    to other nodes.
    @param G: The NetworkX graph.
    """ 
    remove_nodes = []
    for node_degree in G.degree(weight = 'weight'):
        if node_degree[1] == 0:
            remove_nodes.append(node_degree[0])                                             # Node with degree zero, have no connection.

    G.remove_nodes_from(remove_nodes)

# This function is from the Bachelor Thesis of Joy Kwant
def girvan_list_csv(G, folder_name):
    """ Performs the Girvan Newman algorithm from NetworkX. After each iteration, the outcome
    will be imported to a csv file.
    @param G: The NetworkX graph.
    """ 
    remove_noise(G)
    print("in girvan")
    gn = girvan_newman(G)                                                                   # Returns an iterator.
    print("gn done nice")

    for i in range(1,3):
        print(i)
        t = tuple(sorted(c) for c in next(gn))
        print("Going in the open ")
        with open(r"csv\girvan_newman_t="+ str(i) +"_" + folder_name + ".csv", "w") as f:
            csv_writer = csv.writer(f)
            print("in the open ", t)
            csv_writer.writerow(t)
            i = i + 1



def community_metric_report(G, folder_name):
    # girvan_list_csv(G, folder_name)
    # Louvain is already in the plot_communities

    # Homophily analysis
    # Count edges (connections) where nodes (users) share the same timezone
    homophily_edges = sum(1 for u, v in G.edges() if G.nodes[u]['time_zone'] == G.nodes[v]['time_zone'])
    total_edges = G.number_of_edges()
    homophily_ratio = homophily_edges / total_edges if total_edges > 0 else 0
    print("Homophily Ratio:", homophily_ratio)

    # # Calculate betweenness centrality for nodes
    # betweenness = nx.betweenness_centrality(G)

    # # Identify nodes with high betweenness centrality (putin = 0.025 (3 bridges), german = 0.0001 (38 bridges), charlie = 0.003 (62 bridges))
    # bridge_nodes = [node for node, centrality in betweenness.items() if centrality > 0.025]
    # print("The number of Bridge nodes:", len(bridge_nodes))

def girvan_list_from_csv(gn_list, folder_name):
    """ Imports the Girvan Newman clustering of one iteration.
    @param gn_list: Empty list for the Girvan Newman communites list.
    """
    with open(r"csv\girvan_newman_t=1_" + folder_name + ".csv", newline='') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            for item in row:  # Each item in `row` is a string representation of a list
                community = ast.literal_eval(item)  # Convert string to list of node IDs
                gn_list.append(community)

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


# This function is from Bachelor Thesis of Joy Kwant
def plot_community_graph(G, FOLDER, network, c_name = ' ',):
    """ Plots the graph G.
    @param G: The NetworkX graph.
    @param c_name: The name of the community method.
    @param
    """ 
    pos = {}
    fig, ax = plt.subplots(figsize=(12, 7))
    
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}                             # Title/legend.
    font["color"] = "black"                                                                 # Change font color for legend.
    
    csv_dict_position(pos, FOLDER + "_" + network)                                          # Fetch postions.
    node_color = []                                                                         # Initialize list for node colors.
    
    if 'putin' in FOLDER:
        print("delete")
        del color_list[8]
        if "Girvan" in c_name: 
            del color_list[5]
            del color_list[11]
    

    # Plotting community colors if true.
   
    cluster_list = []
    matchpatch_list = []
    dict_node_color = {}
    com = 0
    total_members = 0
    
    if c_name == 'Girvan Newman':
    # Plotting the clustering of girvan newman algorithm.
        girvan_list_from_csv(cluster_list, FOLDER + "_" + network)                                      # Imports Girvan Newman communities from csv file.
        #remove_noise(G)                                                                                # Noise is not in Girvan Newman.
    elif c_name == 'Louvain':
        cluster_list = nx.community.louvain_communities(G, weight= 'weight', seed=101)

    print(len(cluster_list))

    # Assign colors to each node per community in a seperate dictionary.
    for community in cluster_list:
        members = 0
        for n_id in community:
            dict_node_color[n_id] = color_list[com + 1]
            members = members + 1
        
        # Add mpatch to list for legend.
        #if members >= 500:
        community_color = mpatches.Patch(color = color_list[com + 1], label = 'Com. ' + str(com+1) + ', ' + r"$\rho$"+ ' = ' + str(members))
        matchpatch_list.append(community_color)    
        com = com + 1
        total_members += members  
     
    
    node_color = [dict_node_color[n] for n in G.nodes()]                                # List of colors.

    avg_member = int(total_members/com + 1)

    # Set title.
    if c_name == 'Girvan Newman':    
        ax.set_title(f"Folder: {FOLDER}, communties by the {c_name}, iteration = 1, of network of {network},\n with a total of {com} communties and an average of {avg_member} members per community", font)
    else:
        ax.set_title(f"Folder: {FOLDER}, communties by the {c_name} of network of {network},\n with a total of {com} communties and an average of {avg_member} members per community", font)
    # Set legend.
    ax.legend(handles = matchpatch_list)                                  
  
    node_size = 20

    nx.draw_networkx(
        G,
        pos = pos,
        with_labels = False,
        node_color = node_color,
        node_size = node_size,
        edge_color = "gainsboro",
        alpha = 0.4,
    )

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    # Change font color for legend
    font["color"] = "b"


    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")

    plt.show()





