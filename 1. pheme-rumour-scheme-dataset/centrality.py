import networkx as nx
import operator



def take_weight(tup):
    """ Takes the second element from tuple for sorting, (actor_id, weight).
    @param tup: The tuple.
    @returns The second element of the tuple.
    """
    return tup[1]



# DEGREE

def degree_weighted_list(G, graph_name):
    """ Calculates the weighted degree of each node in graph G
    and exports the outcome to a csv file.
    @param G: The NetworkX graph.
    @param graph_name: The name of graph (AA, DA, ..).
    """ 
    degree_weight = list(G.degree(weight='weight'))

    # Export dictionary, right order for the postions of nodes for plotting graphs.
    with open('dict_degree_weight_'+ graph_name + '.csv', 'w') as f:
        for tup in degree_weight:
            f.write("%s,%s\n"%(tup[0],tup[1]))

    degree_weight.sort(key = take_weight, reverse = True)

    # Put Descending list in csv.
    with open('degree_weight_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in degree_weight))
  


def centrality_degree_unweight(G, graph_name):
    """ Performs the degree centrality, unweighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    @param G: The NetworkX graph.
    @param graph_name: The name of graph (AA, DA, ..).
    """  
    centrality_degree = nx.degree_centrality(G)

    # Export dictionary, right order for the postions of nodes for plotting graphs.
    with open('dict_degree_unweighted_'+ graph_name + '.csv', 'w') as f:
        for key in centrality_degree.keys():
            f.write("%s,%s\n"%(key,centrality_degree[key]))

    # Sorts the dictionary in descending order, returns list.
    centrality_degree = sorted(centrality_degree.items(), key = operator.itemgetter(1), reverse = True)
    
    with open('degree_unweighted_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in centrality_degree))

    top_ten_degree = centrality_degree[:10]
    print("Top ten is \n", top_ten_degree)



# BETWEENNESS

def centrality_betweenness_weight(G, graph_name):
    """ Performs the betweenness centrality, weighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.

    Disclaimer, running time was 4 hours and 45 min for AA network!

    @param G: The NetworkX graph.
    @param graph_name: The name of graph (AA, DA, ..)
    """ 
    betweenness_weight = nx.betweenness_centrality(G, weight= 'weight')

    # Export dictionary, right order for the postions of nodes for plotting graphs.
    with open('dict_betweenness_weight_'+ graph_name + '.csv', 'w') as f:
        for key in betweenness_weight.keys():
            f.write("%s,%s\n"%(key,betweenness_weight[key]))

    # Sorts the dictionary in descending order, returns list.
    betweenness_weight = sorted(betweenness_weight.items(), key = operator.itemgetter(1), reverse = True)

    with open('betweenness_weight_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in betweenness_weight))

    top_ten_betweenness = betweenness_weight[:10]
    print("Top ten is \n", top_ten_betweenness)             



# CLOSENESSS

def centrality_closeness_weight(G, graph_name):
    """ Performs the closeness centrality, weighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.

    Disclaimer, running time was 3 hours and 12 min for AA network!

    @param G: The NetworkX graph.
    @param graph_name: name of graph (AA, DA, ..)..
    """
    closeness_weight = nx.closeness_centrality(G, distance = 'weight')
    
    # Export dictionary, right order for the postions of nodes for plotting graphs
    with open('dict_clossness_weight_'+ graph_name + '.csv', 'w') as f:
        for key in closeness_weight.keys():
            f.write("%s,%s\n"%(key,closeness_weight[key]))

    # Sorts the dictionary in descending order, returns list.
    closeness_weight = sorted(closeness_weight.items(), key = operator.itemgetter(1), reverse = True)

    with open('closeness_weight_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in closeness_weight))

    top_ten_closeness = closeness_weight[:10]
    print("Top ten is \n", top_ten_closeness) 



# EIGEN VECTOR

def centrality_eigenvector_weight(G, graph_name):
    """ Performs the eigenvector centrality, weighted, of NetworkX on graph G
    and exports the outcome as dictionary and in descending order to a csv file.
    @param G: The NetworkX graph.
    @param graph_name: The name of graph (AA, DA, ..).
    """ 
    eigenvector_weight = nx.eigenvector_centrality(G, weight = 'weight')

    # Export dictionary, right order for the postions of nodes for plotting graphs
    with open('dict_eigenvector_weight_'+ graph_name + '.csv', 'w') as f:
        for key in eigenvector_weight.keys():
            f.write("%s,%s\n"%(key,eigenvector_weight[key])) 

    # Sorts the dictionary in descending order, returns list.
    eigenvector_weight = sorted(eigenvector_weight.items(), key = operator.itemgetter(1), reverse = True)

    with open('eigenvector_weight_desc_'+ graph_name + '.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in eigenvector_weight))

    top_ten_closeness = eigenvector_weight[:10]
    print("Top ten is \n", top_ten_closeness)  



def all_centralities(G, graph_name):
    """ Runs all centralities.
    @param G: The NetworkX Graph.
    @param graph_name: The name of graph (AA, DA, ..).
    """
    centrality_degree_unweight(G, graph_name)
    centrality_eigenvector_weight(G, graph_name)
    centrality_closeness_weight(G, graph_name)
    centrality_betweenness_weight(G, graph_name)