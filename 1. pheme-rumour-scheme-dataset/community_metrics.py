import csv
import operator
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
    """ Preforms the Grivan Newman algorithm from NetworkX. After each iteration, the outcome
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