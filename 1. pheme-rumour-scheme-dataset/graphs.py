import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms.community.centrality import girvan_newman
import random
import operator
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

import csv_files

# For Clustering
colors = mcolors.CSS4_COLORS
html_colors = list(colors.values())[10:]
color_list = html_colors
del color_list[13:17]

# Different node colors
actor_color = '#BF0A8E'     # Color purple/pink
director_color = '#0ABF3B'  # COlor green



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



def add_edges(film_dictionary, G):
    """ Places edges in graph between two actors who played in the same film.
    @param film_dictionary: The film dictionary containing films with actors.
    @param G: The NetworkX graph.
    """ 
    for key in film_dictionary.copy():
        actor_list = film_dictionary[key]
        if(len(actor_list) != 1):
            for i in range(0, len(actor_list)):
                for j in range(i+1, len(actor_list)):
                    first_node = actor_list[i]
                    second_node = actor_list[j]
                    place_edge(G, first_node, second_node)



def add_edges_actor_director(film_dictionary, director_directory, DA):
    """ Places edges in graph between an actor and a director who worked on the same film.
    @param film_dictionary: The film dictionary containing films with actors.
    @param director_dictionary: The director dictionary containing films with directors.
    @param DA: The DA graph
    """ 
    c = 0
    ac_dir = []
    for key in film_dictionary:
        actor_list = film_dictionary[key]
        director_list = director_directory[key]
        for actor in actor_list:
            for director in director_list:
                if actor != director:
                    place_edge(DA, actor, director)
                else:
                    ac_dir.append(actor)              

    print("Directors who play in there own film: ", len(ac_dir))

    # No director-director linked from the directors list
                


def maximum_weighted_edges(Graph):
    """ Creates a list of triple tuples in descending order of highest weighted edges between two actors to lowest,
    and import it in a csv file.
    @param Graph: The netwrokX graph of which the user wants the list of the descending order of maximum weights of.
    """ 
    # List of triple tuples : (D/A, D/A, weight)
    edges_Graph = sorted(Graph.edges(data=True), key= lambda t: t[2]['weight'], reverse= True)
    with open('max_edge_DA.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]},{tup[2]}' for tup in edges_Graph))            



def maximum_weighted_edges_DA(DA):
    """ Creates a list of triple tuples in descending order of highest weighted edges between an actor and a director to lowest,
    and import it in a csv file.    
    @param DA: The DA graph.
    """
    edges_DA = sorted(DA.edges(data=True), key= lambda t: t[2]['weight'], reverse= True)
    
    actors_DA = []

    for edge_tup in edges_DA:
        first_act_or_dir = edge_tup[0]
        second_act_or_dir = edge_tup[1]
        if DA.nodes[first_act_or_dir]['label'] == 'actor' or DA.nodes[second_act_or_dir]['label'] == 'actor':
            actors_DA.append(edge_tup)

    with open('max_edge_DA_actors_director.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]},{tup[2]}' for tup in actors_DA))
 


def connected_components(G):
    """ Prints the list of connected components.
    @param G: The NetworkX graph.
    """
    cc = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    print("Graph has "+ str(len(cc)) + " connected components:")
    print(cc)



# CLUSTERING

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



def girvan_list_csv(G):
    """ Preforms the Grivan Newman algorithm from NetworkX. After each iteration, the outcome
    will be imported to a csv file.
    ! DISCLAIMER XL: For the AA graph it took 12 hours for the first 2 iterations, but 
    the algortihm was still at 30 hours for the third iteration, but did not finish. 
    Therefore kept the print statements.
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
        with open("girvan_newman_t="+ str(i) +".csv", "w") as f:
            csv_writer = csv.writer(f)
            print("in the open ", t)
            csv_writer.writerow(t)
            i = i + 1



def cluster_coefficient_weighted(G):
    """ Perfoms the cluster coefficient on grpah G, with the weight attribute of the edges,
    and stores the outcome in descending order and as dictionary in csv files.
    @param G: The NetworkX graph.
    """ 
    cc_weigth = nx.clustering(G, weight= 'weight')

    with open('dict_clustercoeff_weight.csv', 'w') as f:
        for key in cc_weigth.keys():
            f.write("%s,%s\n"%(key,cc_weigth[key])) 

    cc_weigth = sorted(cc_weigth.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open('clustercoeff_weight_desc.csv', 'w') as f:
       f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in cc_weigth))

    top_ten_cc = cc_weigth[:10]
    print("Top ten is \n", top_ten_cc)    

  

def louvain(G):
    """ Perform the Louvain algorithm for clustering of graph G, with the weight attribute of the edges,
    and stores the outcome list in a csv file.
    @param G: The NetworkX graph.
    """ 
    louvain_list = nx.community.louvain_communities(G, weight= 'weight', seed=101)
    with open("louvain.csv", "w") as f:
        f.write('\n'.join(f'{community}' for community in louvain_list))
  


# LINK ANALYSIS

def hits(G, graph_name):
    """ Perform the HITS algorithm on graph G, but first converts undirected graph to directed graph,
    and stores the outcome of the Hubs and Authorities in descending order in csv files.
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G (AA, DA, ..). 
    """ 
    print("in hits")
    H = G.to_directed()                                                                     # Converts undirected graph to a directed graph.
    h, a = nx.hits(H)                                                                       # Returns two dictionaries of Hubs and Authorities.

    print("sorted")
    h = sorted(h.items(), key = operator.itemgetter(1), reverse = True)
    a = sorted(a.items(), key = operator.itemgetter(1), reverse = True)


    with open('hits_hubs_' + graph_name + '.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in h))

    with open('hits_authorities_' + graph_name + '.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in a))        
    


def pagerank(G, graph_name):
    """ Performs the Page Rank on the graph G, with the weight attributes of the edges,
    and stores the outcome in descending order in a csv file.
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G (AA, DA, ..).
    """ 
    pr = nx.pagerank(G, weight = 'weight')
    pr_desc = sorted(pr.items(), key = operator.itemgetter(1), reverse = True)

    with open('pagerank_' + graph_name + '.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in pr_desc))    



# PLOTTING

def remove_noise_plotting_graph(centrality_dictionary, G):
    """ Removes the nodes with zero values from the graph and in the centrality dictionary.
    @param centrality_dictionary: The dictionary containing the centrality values.
    @param G: The NetworkX graph.
    """ 
    remove_nodes = []
    for key in centrality_dictionary.copy():
        if centrality_dictionary[key] == 0:
            remove_nodes.append(key)
            centrality_dictionary.pop(key)                                                  # Remove from centrality.

    G.remove_nodes_from(remove_nodes)                                                       # Remove from graph.


def fetch_centrality_multiplier(centrality_name):
    """ Returns the right multiplier for each centraility name.
    @param centrality_name: The name of the centrality metric.
    @returns the centrality multiplier.
    """ 
    if centrality_name == 'Degree': return 10000
    elif centrality_name == 'Betweenness': return 250000
    elif centrality_name == 'Closeness': return 200
    elif centrality_name == 'Eigenvector': return 100000
    else: return 10



def plot_graph(community, centrality, G, c_name = ' ', centrality_filename = ' '):
    """ Plots the graph G.
    @param community: Boolean of whether communities should be shown.
    @param centrality: Boolean of wheter the centrality should be taken into account of plotting the nodes.
    @param G: The NetworkX graph.
    @param c_name: The name of the centrality metric or the community method.
    @param centrality_filename: The name of the csv where the dictionary of the centrality is stored.
    """ 
    pos = {}
    fig, ax = plt.subplots(figsize=(20, 15))
    
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}                             # Title/legend.
    font["color"] = "black"                                                                 # Change font color for legend.
    
    csv_files.csv_dict_position(pos, 'AA')                                                  # Fetch postions.
    node_color = []                                                                         # Initialize list for node colors.
    
    # Plotting centrality if true.
    if centrality:  
        centrality_dictionary = {}                                                          
        csv_files.csv_dict_centrality(centrality_dictionary, centrality_filename)           # Imports centrality dictionary.
        remove_noise_plotting_graph(centrality_dictionary, G)
        centrality_mutiplier = fetch_centrality_multiplier(c_name)
        node_size = [v*centrality_mutiplier for v in centrality_dictionary.values()]      
    else:                                                                                   # Plotting a normal graph.
        node_size = 10

    # Plotting community colors if true.
    if community:
        cluster_list = []
        matchpatch_list = []
        dict_node_color = {}
        com = 0
        
        if c_name == 'Girvan Newman':
        # Plotting the clustering of girvan newman algorithm.
            csv_files.girvan_list_from_csv(cluster_list)                                    # Imports Girvan Newman communities from csv file.
            remove_noise(G)                                                                 # Noise is not in Girvan Newman.
        elif c_name == 'Louvain':
            cluster_list = nx.community.louvain_communities(G, weight= 'weight', seed=101)

        # Assign colors to each node per community in a seperate dictionary.
        for community in cluster_list:
            members = 0
            for actor_id in community:
                dict_node_color[actor_id] = color_list[com + 1]
                members = members + 1
           
            # Add mpatch to list for legend.
            community_color = mpatches.Patch(color = color_list[com + 1], label = 'Com. ' + str(com+1) + ', ' + r"$\rho$"+ ' = ' + str(members))
            matchpatch_list.append(community_color)    
            com = com + 1    
        
        node_color = [dict_node_color[n] for n in G.nodes()]                                # List of colors.

        # Set title.
        ax.set_title('Actors network, '+ c_name + ' with ' + str(com) + ' communities and k=1', font)
        # Set legend.
        ax.legend(handles = matchpatch_list, ncol = 2)                                  
  
    else:
        node_color = [actor_color for n in G.nodes()]                                       # List of colors.
       
        # Set title.
        if centrality:    
            ax.set_title('Actors network with ' + c_name + ' centrality in period 1910-2021', font)
        else:
            ax.set_title("Actors network in period 1910-2021", font)
    
        # Set legend.
        actor_node_color = mpatches.Patch(color = actor_color, label = 'Actor')
        ax.legend(handles=[actor_node_color])


    nx.draw_networkx(
        G,
        pos = pos,
        with_labels = False,
        node_color = node_color,
        node_size = node_size,
        edge_color = "gainsboro",
        alpha = 0.4,
    )

    # # Title/legend
    # font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    # # Change font color for legend
    # font["color"] = "r"

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")

    plt.show()



def plot_graph_year(pos, year, Y, louvain):
    """ Plot Year Graph.
    @param pos: List of the postions of each node in the graph.
    @param year: The year key.
    @param Y: The NetworkX graph.
    @param louvain: Boolean, whether the louvain communities needs to be computed and shown.
    """ 
    fig, ax = plt.subplots(figsize=(20, 15))
    
    node_size = 10
    node_color = [actor_color for n in Y.nodes()]

    font = {"color": "k", "fontweight": "bold", "fontsize": 10}                             # Title/legend.

    if louvain:
        matchpatch_list = []
        louvain_list = nx.community.louvain_communities(Y, weight= 'weight', seed=101)      # Computes the Louvain communities.
        dict_node_color = {}
        com = 0
        
        for community_set in louvain_list:
            members = 0
            for a_id in community_set:
                dict_node_color[a_id] = color_list[com + 1]
                members = members + 1

            if(members > 1):                                                                # Only include communities with more than one member in the legend.
                community_color = mpatches.Patch(color = color_list[com + 1], label = 'Com. ' + str(com+1) + ', ' + r"$\rho$"+ ' = ' + str(members))
                matchpatch_list.append(community_color)    
            com = com + 1    
        

        node_color = [dict_node_color[n] for n in Y.nodes()]

        # Title/legend.
        ax.set_title("Actors network normal in year period: 1910 - " + str(year) + ", with " + str(com) + " communities", font)
        # Set legend.
        ax.legend(handles = matchpatch_list, ncol = 2)
    
    else:
        # Title/legend.
        ax.set_title("Actors network normal in year period: 1910 - " + str(year), font)
        actor_node_color = mpatches.Patch(color = actor_color, label = 'Actor')
        ax.legend(handles=[actor_node_color])                                                     
        
    nx.draw_networkx(
        Y,
        pos = pos,
        with_labels = False,
        node_size = node_size,
        node_color = node_color,
        edge_color = "gainsboro",
        alpha = 0.4,
    )

    # Change font color for legend.
    font["color"] = "r"

    # Resize figure for label readability.
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")



def plot_graph_DA(DA):
    """ Plots the normal DA graph, no communites or centralities.
    @param DA: The DA graph that needs to be visualized.
    """ 
    pos = {}
    node_size = 10
    node_color = []

    fig, ax = plt.subplots(figsize=(20, 15))
    csv_files.csv_dict_position(pos, 'DA')                                                  # Fetch postions list from csv file.

    for n in DA.nodes(data=True):
        if n[1]['label'] == 'director':
            node_color.append(director_color)
            director_node_color = mpatches.Patch(color = director_color, label = 'Directors')
        elif n[1]['label'] == 'actor':
            node_color.append(actor_color)
            actor_node_color = mpatches.Patch(color = actor_color, label = 'Actor')

    nx.draw_networkx(
        DA,
        pos = pos,
        with_labels = False,
        node_color = node_color,
        node_size = node_size,
        edge_color = "gainsboro",
        alpha = 0.4,
    )

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 10}
    ax.set_title("Directors and Actors network in period 1910-2021", font)
    # Change font color for legend
    font["color"] = "r"
    ax.legend(handles=[actor_node_color, director_node_color])

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")
    plt.show()