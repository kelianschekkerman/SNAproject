### This file is from the Bachelor Thesis of Joy Kwant ###
import networkx as nx
import operator

G = nx.Graph()

# DEGREE
def centrality_degree_unweight(G, graph_name):
    """ 
    Performs the degree centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of graph.
    """  
    centrality_degree = nx.degree_centrality(G)

    # Sorts the dictionary in descending order, returns list.
    centrality_degree = sorted(centrality_degree.items(), key = operator.itemgetter(1), reverse = True)
    
    with open(r'csv\degree_unweighted_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]}, {tup[1]}' for tup in centrality_degree))

    top_ten_degree = centrality_degree[:10]
    print("Top ten degree is \n", top_ten_degree)

    return top_ten_degree


# BETWEENNESS
def centrality_betweeness_list(G, graph_name):
    """ 
    Performs the betweenness centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of graph.
    """    
    centrality_betweeness = nx.betweenness_centrality(G)

    # Sorts the dictionary in descending order, returns list.
    centrality_betweeness = sorted(centrality_betweeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open(r'csv\betweeness_centrality_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]}, {tup[1]}' for tup in centrality_betweeness))

    top_ten_betweeness = centrality_betweeness[:10]
    print("Top ten betweeness is \n", top_ten_betweeness)

    return top_ten_betweeness


# CLOSENESSS
def centrality_closeness_list(G, graph_name):
    """ 
    Performs the closeness centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of graph.
    """  
    centrality_closeness = nx.closeness_centrality(G)

    # Sorts the dictionary in descending order, returns list.
    centrality_closeness = sorted(centrality_closeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open(r'csv\closeness_centrality_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]}, {tup[1]}' for tup in centrality_closeness))

    top_ten_closeness = centrality_closeness[:10]
    print("Top ten closeness is \n", top_ten_closeness)  

    return top_ten_closeness


# EIGEN VECTOR
def centrality_eigenvector_list(G, graph_name):
    """ 
    Performs the eigenvector centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of graph.
    """  
    centrality_eigenvector = nx.eigenvector_centrality(G, max_iter=500)
    centrality_eigenvector = sorted(centrality_eigenvector.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open(r'csv\eigenvector_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]}, {tup[1]}' for tup in centrality_eigenvector))

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