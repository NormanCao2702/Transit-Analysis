# Transit-Analysis

Order of executing the file:

- There are only 3 files that you need to execute, those are: csv_producing.py, cluster_mapping.py, main.py
- The order for you to successfully obtain the results are:

1. csv_producing.py
2. cluster_mapping.py
3. main.py

Explaination:

1. Firstly, you need to run the code csv_producing.py by running the script `python3 csv_producing.py`, this is for producing csv file that needed to plot heatmap on interval of buses to SFU as well as statistical analysis.
2. Secondly, you need to run cluster_mapping.py `python3 cluster_mapping.py`,this is to map the result of clustering of those csv files.
3. Finally, running `main.py` for plotting heatmap as well as the histogram of wait times for each buses.

Note:

- All of the csv file will be stored in csv folder.
- All of cluster result will be stored in schedule-cluster.
- All of heatmap plot will be stored in heatmap-pic.
- All of bus histogram will be stored in bus-histogram.
