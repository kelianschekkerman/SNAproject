import networkx as nx
import operator

G = nx.Graph()

# BETWEENESS

# Disclaimer, running the betweeness for G was with a running time of almost 2 hours ( 1:50:00 - 1:59:00)
def centrality_betweeness_list():
    centrality_betweeness = nx.betweenness_centrality(G)
    centrality_betweeness = sorted(centrality_betweeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('betweeness_centrality_desc.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_betweeness))

    top_ten_betweenness = centrality_betweeness[:10]
    print("Top ten is \n", top_ten_betweenness)



# CLOSENESSS

# Disclaimer, running time was 55 min
def centrality_closeness_list():
    centrality_closeness = nx.closeness_centrality(G)
    centrality_closeness = sorted(centrality_closeness.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('closeness_centrality_desc.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_closeness))

    top_ten_closeness = centrality_closeness[:10]
    print("Top ten is \n", top_ten_closeness)  



# EIGEN VECTOR


# running time less than 30 seconds
def centrality_eigenvector_list():
    centrality_eigenvector = nx.eigenvector_centrality(G)

    with open('dict_eigenvector.csv', 'w') as f:
        for key in centrality_eigenvector.keys():
            f.write("%s,%s\n"%(key,centrality_eigenvector[key])) 

    #print("Degree of Nodes of G = \n", centrality_betweeness)
    centrality_eigenvector = sorted(centrality_eigenvector.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('eigenvector_desc.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in centrality_eigenvector))

    top_ten_closeness = centrality_eigenvector[:10]
    print("Top ten is \n", top_ten_closeness) 
