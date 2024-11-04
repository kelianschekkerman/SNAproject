# Analysing Information Spread and Community Dynamics on Twitter during Breaking News Events

The code of the project is in the folder `PHEME Project`. The data of the tweet threads are in the folder `threads`, used to for the network creation and analysis.
We have data from twitter threads of three breaking news events: Putin missing, Germanwings crash and Charlie Hebdo.

In the `main.py` and `tweetdistribution.py` you can pick a breaking news event:
```
# The different breaking news events
charlie = 'charliehebdo'
german_airplane = 'germanwings-crash'
putin = 'putinmissing'

# Pick a folder
FOLDER = german_airplane
``` 

### Main.py
In the `main.py` is the creation and visualization of networks: tweet or following network. You can also retrieve the metric and/or community report, and plot the communitites. This can be done using the following global variables:
```
# For calling functions
CREATION_TWEETS_NETWORK = False
CREATION_FOLLOWING_NETWORK = True
METRICS_REPORT = False
COMMUNITY_REPORT = False
PLOT_COMMUNITIES = True
```
`METRICS_REPORT` uses the files `metrics.py` and `centrailties_unweighted.py`. `COMMUNITY_REPORT` and `PLOT_COMMUNITIES` use the file `community_metrics.py`


### Tweetdistribution.py
In the `tweetdistribution.py` you can get the tweet distribution overtime and the tweet statistics. This can be done using the following global variables:
```
# Two options for getting different information:
ITERATIONS_DISTRIBUTION = True
STATISTICS = True
```

### Getplotfromcsv.py
We used this file to plot the results of centrality and hits scores for the three events. This file is not part of the functionality of the code. 


### README of PHEME
In the folder `PHEME Project` the original README of the PHEME rumour scheme dataset can be found that describes the structure of the dataset and corresponding annotations.