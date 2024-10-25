
### This file is from the Bachelor Thesis of Joy Kwant ###

import networkx as nx
import operator

G = nx.Graph()

# DEGREE
def centrality_degree_unweight(G, graph_name):
    """ Performs the degree centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    @param G: The NetworkX graph.
    @param graph_name: The name of graph (AA, DA, ..).
    """  
    centrality_degree = nx.degree_centrality(G)

    # Export dictionary, right order for the postions of nodes for plotting graphs.
    # with open('dict_degree_unweighted_'+ graph_name + '.csv', 'w') as f:
    #     for key in centrality_degree.keys():
    #         f.write("%s,%s\n"%(key,centrality_degree[key]))

    # Sorts the dictionary in descending order, returns list.
    centrality_degree = sorted(centrality_degree.items(), key = operator.itemgetter(1), reverse = True)
    
    with open('csv\degree_unweighted_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in centrality_degree))

    top_ten_degree = centrality_degree[:10]
    print("Top ten degree is \n", top_ten_degree)

    return top_ten_degree


# BETWEENESS

# Disclaimer, running the betweeness for G was with a running time of almost 2 hours ( 1:50:00 - 1:59:00)
def centrality_betweeness_list(G, graph_name):
    centrality_betweeness = nx.betweenness_centrality(G)
    centrality_betweeness = sorted(centrality_betweeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('csv\betweeness_centrality_desc_'+ graph_name + '-.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_betweeness))

    top_ten_betweenness = centrality_betweeness[:10]
    print("Top ten betweeness is \n", top_ten_betweenness)

    return top_ten_betweenness



# CLOSENESSS

# Disclaimer, running time was 55 min
def centrality_closeness_list(G, graph_name):
    centrality_closeness = nx.closeness_centrality(G)
    centrality_closeness = sorted(centrality_closeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('csv\closeness_centrality_desc_'+ graph_name + '_.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_closeness))

    top_ten_closeness = centrality_closeness[:10]
    print("Top ten closeness is \n", top_ten_closeness)  

    return top_ten_closeness



# EIGEN VECTOR


# running time less than 30 seconds
def centrality_eigenvector_list(G, graph_name):
    centrality_eigenvector = nx.eigenvector_centrality(G, max_iter=500)

    # with open('dict_eigenvector.csv', 'w') as f:
    #     for key in centrality_eigenvector.keys():
    #         f.write("%s,%s\n"%(key,centrality_eigenvector[key])) 

    #print("Degree of Nodes of G = \n", centrality_betweeness)
    centrality_eigenvector = sorted(centrality_eigenvector.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('csv\eigenvector_desc_'+ graph_name + '_.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_eigenvector))

    top_ten_eigenvector = centrality_eigenvector[:10]
    print("Top ten eigenvector is \n", top_ten_eigenvector) 

    return top_ten_eigenvector



def all_centralities(G, graph_name):
    """ Runs all centralities.
    @param G: The NetworkX Graph.
    @param graph_name: The name of graph.
    """
    top_ten_degree =  centrality_degree_unweight(G, graph_name)
    top_ten_betweenness = centrality_betweeness_list(G, graph_name)
    top_ten_closeness = centrality_closeness_list(G, graph_name)
    top_ten_eigenvector = centrality_eigenvector_list(G, graph_name)

    return top_ten_degree, top_ten_betweenness, top_ten_closeness, top_ten_eigenvector