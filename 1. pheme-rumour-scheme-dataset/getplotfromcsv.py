import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Define file paths
file_paths = {
    "charlie_following_betweenness": "csv/charlie_following/betweeness_centrality_desc_charliehebdo_following.csv",
    "charlie_following_closeness": "csv/charlie_following/closeness_centrality_desc_charliehebdo_following.csv",
    "charlie_following_degree": "csv/charlie_following/degree_unweighted_desc_charliehebdo_following.csv",
    "charlie_following_eigenvector": "csv/charlie_following/eigenvector_desc_charliehebdo_following.csv",
    
    "charlie_tweets_betweenness": "csv/charlie_tweets/betweeness_centrality_desc_charliehebdo_tweets.csv",
    "charlie_tweets_closeness": "csv/charlie_tweets/closeness_centrality_desc_charliehebdo_tweets.csv",
    "charlie_tweets_degree": "csv/charlie_tweets/degree_unweighted_desc_charliehebdo_tweets.csv",
    "charlie_tweets_eigenvector": "csv/charlie_tweets/eigenvector_desc_charliehebdo_tweets.csv",

    "germanwings_crash_following_betweenness": "csv/german-wing_following/betweeness_centrality_desc_germanwings-crash_following.csv",
    "germanwings_crash_following_closeness": "csv/german-wing_following/closeness_centrality_desc_germanwings-crash_following.csv",
    "germanwings_crash_following_degree": "csv/german-wing_following/degree_unweighted_desc_germanwings-crash_following.csv",
    "germanwings_crash_following_eigenvector": "csv/german-wing_following/eigenvector_desc_germanwings-crash_following.csv",

    "germanwings_crash_tweets_betweenness": "csv/german-wings_tweets/betweeness_centrality_desc_germanwings-crash_tweets.csv",
    "germanwings_crash_tweets_closeness": "csv/german-wings_tweets/closeness_centrality_desc_germanwings-crash_tweets.csv",
    "germanwings_crash_tweets_degree": "csv/german-wings_tweets/degree_unweighted_desc_germanwings-crash_tweets.csv",
    "germanwings_crash_tweets_eigenvector": "csv/german-wings_tweets/eigenvector_desc_germanwings-crash_tweets.csv",

    "putin_following_betweenness": "csv/putin_following/betweeness_centrality_desc_putinmissing_following.csv",
    "putin_following_closeness": "csv/putin_following/closeness_centrality_desc_putinmissing_following.csv",
    "putin_following_degree": "csv/putin_following/degree_unweighted_desc_putinmissing_following.csv",
    "putin_following_eigenvector": "csv/putin_following/eigenvector_desc_putinmissing_following.csv",

    "putin_tweets_betweenness": "csv/putin_tweets/betweeness_centrality_desc_putinmissing_tweets.csv",
    "putin_tweets_closeness": "csv/putin_tweets/closeness_centrality_desc_putinmissing_tweets.csv",
    "putin_tweets_degree": "csv/putin_tweets/degree_unweighted_desc_putinmissing_tweets.csv",
    "putin_tweets_eigenvector": "csv/putin_tweets/eigenvector_desc_putinmissing_tweets.csv",
}

# Define plot configurations
plot_configs = [
    # Following data
    ("Following Betweenness", ["charlie_following_betweenness", "germanwings_crash_following_betweenness", "putin_following_betweenness"]),
    ("Following Closeness", ["charlie_following_closeness", "germanwings_crash_following_closeness", "putin_following_closeness"]),
    ("Following Degree", ["charlie_following_degree", "germanwings_crash_following_degree", "putin_following_degree"]),
    ("Following Eigenvector", ["charlie_following_eigenvector", "germanwings_crash_following_eigenvector", "putin_following_eigenvector"]),
    
    # Tweets data
    ("Tweets Betweenness", ["charlie_tweets_betweenness", "germanwings_crash_tweets_betweenness", "putin_tweets_betweenness"]),
    ("Tweets Closeness", ["charlie_tweets_closeness", "germanwings_crash_tweets_closeness", "putin_tweets_closeness"]),
    ("Tweets Degree", ["charlie_tweets_degree", "germanwings_crash_tweets_degree", "putin_tweets_degree"]),
    ("Tweets Eigenvector", ["charlie_tweets_eigenvector", "germanwings_crash_tweets_eigenvector", "putin_tweets_eigenvector"])
]

# Load CSV files into a dictionary of DataFrames
dataframes = {name: pd.read_csv(path, header=None) for name, path in file_paths.items()}

# Loop through each plot configuration to create and display each plot
for title, data_keys in plot_configs:
    plt.figure(figsize=(10, 6))
    for key in data_keys:
        # Convert to numpy arrays to avoid multi-dimensional indexing issues
        y_values = np.array(dataframes[key][1])
        x_values = np.arange(len(y_values))
        
        # Plot each data series by switching x and y to rotate the plot
        plt.plot(y_values, x_values, label=key)
    
    # Customize each plot
    plt.title(title)
    plt.ylabel("Nodes (ordered by rank)")
    plt.xlabel("Metric Value")
    plt.xscale("log")  # Apply logarithmic scale to the x-axis
    plt.legend()

    # Save the figure
    filename = f"{title.replace(' ', '_').lower()}.png"  # Replace spaces with underscores and convert to lowercase
    plt.savefig(os.path.join("../Graphs/centralities", filename))

    plt.show()