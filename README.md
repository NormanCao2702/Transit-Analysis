# Transit-Analysis

## Aspect 1: Analysis on SFU Transportation

Order of executing the file:

- There are only 3 files that you need to execute, those are: csv_producing.py, cluster_mapping.py, main.py
- The order for you to successfully obtain the results are:

1. csv_producing.py
2. cluster_mapping.py
3. main.py

Explanation:

1. Firstly, you need to run the code csv_producing.py by running the script `python3 csv_producing.py`, this is for producing csv file that needed to plot heatmap on interval of buses to SFU as well as statistical analysis.
2. Secondly, you need to run cluster_mapping.py `python3 cluster_mapping.py`, this is to map the result of clustering of those csv files.
3. Finally, running `main.py` for plotting heatmap as well as the histogram of wait times for each buses.

Note:

- All of the csv file will be stored in csv folder.
- All of cluster result will be stored in schedule-cluster.
- All of heatmap plot will be stored in heatmap-pic.
- All of bus histogram will be stored in bus-histogram.

## Aspect 2: Comparing Sampled Trip Distances and Average Speeds

Order of executing the files:

- for this section there are 2 python files that need to be executed
- The programs are meant to be run with Python without the need to give any input or output files or directories
- The order of execution is as follows:
  1. python3 gather_region_data.py
  2. python3 analyze_region_data.py

Explanation:

1. Running the program gather_region_data.py will create two csv files that are stored in the directory gathered_region_data/ from the files located in the directory city_stop_data_files/
2. Running the program analyze_region_data.py will create analysis output from the csv files from the previous program and store the information into analysis_region_results/

Note:

- gather_region_data.py will create two csv files that will be stored in gathered_region_data/
- analyze_region_data.py will create analysis outputs and store them in analysis_region_results/, including the following items:
  1. Histograms of created sampled data
  2. ANOVA results for both sampled mean distances and sampled mean speeds as text files
  3. Spiffy plots and text output for the Tukey-U HSD tests
  4. Scatter plot of data with linear regression line of best fit and text file of residual statistical information
