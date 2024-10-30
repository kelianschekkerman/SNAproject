import csv
import numpy as np
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

# This function is from the Bachelor Thesis of Joy Kwant
def remove_noise(G):
    """ For Girvan Newman. Removes nodes from graph with values, which have no connection 
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

# This function is from the Bachelor Thesis of Joy Kwant
def louvain(G, folder_name):
    """ Perform the Louvain algorithm for clustering of graph G, with the weight attribute of the edges,
    and stores the outcome list in a csv file.
    @param G: The NetworkX graph.
    """ 
    louvain_list = nx.community.louvain_communities(G, weight= 'weight', seed=101)
    with open(r"csv\louvain_" + folder_name + ".csv", "w") as f:
        f.write('\n'.join(f'{community}' for community in louvain_list))

def community_metric_report(G, folder_name):
    girvan_list_csv(G, folder_name)

    # Homophily analysis
    # Count edges where nodes share the same group
    # homophily_edges = sum(1 for u, v in G.edges() if G.nodes[u]['group'] == G.nodes[v]['group'])
    # total_edges = G.number_of_edges()
    # homophily_ratio = homophily_edges / total_edges if total_edges > 0 else 0
    # print("Homophily Ratio:", homophily_ratio)

    # Calculate betweenness centrality for nodes
    betweenness = nx.betweenness_centrality(G)

    # Identify nodes with high betweenness centrality
    bridge_nodes = [node for node, centrality in betweenness.items() if centrality > 0.1]  # 0.1 is an example threshold
    print("The number of Bridge nodes:", len(bridge_nodes))






