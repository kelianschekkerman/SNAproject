import csv
import operator
import numpy as np
import networkx as nx
from centralities_unweighted import all_centralities

### The metrics functions used for the analysis and statistics ###

# This function is from the Bachelor Thesis of Joy Kwant
def hits(G, graph_name):
    """ 
    Perform the HITS algorithm on graph G, but first converts undirected graph to directed graph,
    and stores the outcome of the Hubs and Authorities in descending order in csv files.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G for storing outcome values in csv file. 
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
    """ 
    Perfoms the cluster coefficient on graph G and stores the outcome in descending order 
    and as dictionary in csv files.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G for storing outcome values in csv file. 
    """ 
    cc = nx.clustering(G)
    cc = sorted(cc.items(), key = operator.itemgetter(1), reverse = True)

    # Put Descending list in csv
    with open(f'csv\clustercoeff_{graph_name}_desc.csv', 'w') as f:
        f.write('\n'.join(f'{tup[0]},{tup[1]}' for tup in cc))

    # Extract the values (the second element of each tuple) and convert to a NumPy array
    values = np.array([value for _, value in cc])

    # Calculate the average using NumPy
    avg_cc = np.mean(values)

    return avg_cc


# This function is from the Bachelor Thesis of Joy Kwant
def undirected_connected_components(G):
    """ 
    Computes and prints the list of connected components of an undirected network.
    
    @param G: The NetworkX graph.
    """
    cc = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    print("Graph has "+ str(len(cc)) + " connected components:")
    cc_largest = cc[0] if cc else 0
    print(cc)
    return cc, cc_largest


def directed_connected_components(G):
    """ 
    Computes and prints the list of connected components of an directed network.
    
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
    """ 
    Copmutes the diameter of the graph.
    
    @param G: The NetworkX graph.
    """
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


def degree_distribution_undirected(G, G_name):
    """ 
    Computes various degree statistics of an undirected graph and writes the outcomes to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G for storing outcome values in csv file. 
    """ 
    # Calculate degree for each node in the undirected graph
    degrees = dict(G.degree())
    
    # Convert degrees to a list
    degree_values = list(degrees.values())
    
    # Calculate minimum, maximum, average, and median for degrees
    degree_min = min(degree_values)
    write_to_csv_file("Minimum degree", degree_min, G_name)
    degree_max = max(degree_values)
    write_to_csv_file("Maximum degree", degree_max, G_name)
    degree_avg = np.mean(degree_values)
    write_to_csv_file("Average degree", degree_avg, G_name)
    degree_median = np.median(degree_values)
    write_to_csv_file("Median degree", degree_median, G_name)
    
    # Print results
    print("Degree Centrality Distribution:")
    print(f"Minimum: {degree_min}, Maximum: {degree_max}, Average: {degree_avg:.2f}, Median: {degree_median}")


def degree_distribution_directed(G, G_name):
    """ 
    Computes various degree statistics of an directed graph and writes the outcomes to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G for storing outcome values in csv file. 
    """ 

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
    """ 
    Save the result of a metric to a CSV file corresponding to the graph.
    
    @param metric_name: The name of the metric being saved (e.g., "Average degree").
    @param metric_result: The result of the metric.
    @param graph_name: The name of the graph G for storing the metric results in csv file. 
    """ 
    
    with open(f'csv\metrics_report_{graph_name}.csv','a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([metric_name, metric_result])


# METRICS, project instruction #1
def metric_report(G, G_name):
    """ 
    Calculate the following metrics: number of vertices, number of edges,
    degree distribution, centrality indices, clustering coefficient,
    network diameter, density, number of connected components and, size of
    the connected components.
    Save the results of the metrics to a csv file.
    
    @param G: The NetworkX graph.
    @param graph_name: The name of the graph G for storing the metric results in csv file. 
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
    if G.is_directed():
        degree_distribution_directed(G, G_name)
    else:
        degree_distribution_undirected(G, G_name)

    # Centrality indices (node with highest degree)
    # 1. Degree,  2. Betweenness,  3. Closeness and 4. Eigenvector
    top_ten_degree, top_ten_betweenness, top_ten_closeness, top_ten_eigenvector = all_centralities(G, G_name)
    write_to_csv_file("Top ten degree", top_ten_degree, G_name)
    write_to_csv_file("Top ten betweenness", top_ten_betweenness, G_name)
    write_to_csv_file("Top ten closeness", top_ten_closeness, G_name)
    write_to_csv_file("Top ten eigenvector", top_ten_eigenvector, G_name)

    # Clustering coefficient
    top_ten_ccoeff = cluster_coefficient(G, G_name)
    write_to_csv_file("Average cluster coefficient", top_ten_ccoeff, G_name)
    
    # Network diameter
    # Returns the diameter of the graph G.
    diameter = compute_diameter(G)
    write_to_csv_file("Diameter", diameter, G_name)

    # Graph density
    graph_density = nx.density(G)
    write_to_csv_file("Density", graph_density, G_name)
    print(f"The graph density is: {graph_density}")

    top_ten_h, top_ten_a = hits(G, G_name)
    write_to_csv_file("Top ten hits", top_ten_h, G_name)
    write_to_csv_file("Top ten authorities", top_ten_a, G_name)

    # Number and size of connected components
    if not G.is_directed():
        # Undirected graph
        con_comp, cc_largest = undirected_connected_components(G)
        write_to_csv_file("The number of the connected components", len(con_comp), G_name)
        write_to_csv_file("The size of the largest connected component", cc_largest, G_name)
    else:
        # Directed graph: get strongly and weakly connected components
        strong_con_comp, weak_con_comp, scc_largest, wcc_largest = directed_connected_components(G)
        write_to_csv_file("The number of strongly connected components", len(strong_con_comp), G_name)
        write_to_csv_file("The number of weakly connected components", len(weak_con_comp), G_name)
        write_to_csv_file("The size of the largest strongly connected component", scc_largest, G_name)
        write_to_csv_file("The size of the largest weakly connected component", wcc_largest, G_name)