# CMPT 353 PROJECT
# Zachariah Delft, 301386141

# Transit-Analysis

# perform_anova_tukey.py
# Program is meant to do the following
# [1] open sample_data.csv into a pandas dataframe
# [2] Create a histogram of the samples
# [3] Perform ANOVA test on data by column = city (distances and speeds)
# [4] Perform a one-sided t-test (Tukey-U)
# [5] Perform linear regression and find correlation between distance and speed

# Made reference to:
# https://stackoverflow.com/questions/16826711/is-it-possible-to-add-a-string-as-a-legend-item
# https://matplotlib.org/stable/gallery/statistics/histogram_multihist.html
# https://stackoverflow.com/questions/40516810/saving-statmodels-tukey-hsd-into-a-python-pandas-dataframe
# https://python-graph-gallery.com/scatterplot-with-regression-fit-in-matplotlib/
# extensive reference to various source pages

import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Needed Directories
SAMPLES_DIR = '\\gathered_data\\'
OUTPUT_DIR = '\\analysis_results\\'
CWD = os.getcwd()
# Strings used for labels and output names
DIST_STRING = 'Sampled_Max_Distances'
SPEED_STRING = 'Sampled_Avg_Speed'

# Given distance or speed dataset outputs png file of multiple histograms
def createHistograms(data, string):
    print(f' - Visualizing Data for {string.replace("_", " ")}')
    # Create and save histogram of the samples
    figure, axis = plt.subplots(nrows=2, ncols=4)
    figure.suptitle(f'Histogram of Mean {string.replace("_", " ")}')
    figure.set_figheight(15)
    figure.set_figwidth(20)
    figure.tight_layout()
    i = 0
    j = i + 6
    x, y = 0, 0
    while j <= 48:
        if j > 46:
            j = 45
        axis[y, x].hist(data.iloc[:,i:j], bins=25, alpha=0.5)
        axis[y, x].legend(data.iloc[:,i:j].columns, prop={'size':10})
        y = (y+1)
        if y == 2:
            y = 0
            x += 1
        i = i + 6
        j = j + 6
        if not os.path.exists(CWD + OUTPUT_DIR):
            os.mkdir(CWD + OUTPUT_DIR)
        plt.savefig(CWD+OUTPUT_DIR+'f{string.lower()}_histograms.png')

# Given distance or speed data, performs outputs and returns ANOVA statistic and p-value
def performAnova(data, string):
    print(f' - Preforming ANOVA on {string.replace("_", " ")}...')
    anova = stats.f_oneway(data['100 mile house'], data['Agassiz-Harrison'], 
                           data['Ashcroft-Cache-Creek-Clinton'], data['Bulkley Nechako'], 
                           data['Campbell River'], data['Central Fraser Valley'], 
                           data['Chilliwack'], data['Clearwater'], data['Columbia Valley'], 
                           data['Comox Valley'], data['Cowichan Valley'], data['Cranbrook'], 
                           data['Creston Valley'], data['Dawson Creek'], data['Elk Valley'], 
                           data['Fort St John'], data['Greater Vancouver'], data['Hazeltons'], 
                           data['Hope'], data['Kamloops'], data['Kelowna'], data['Kimberley'], 
                           data['Kitimat'], data['Merritt'], data['Mount Waddington'], 
                           data['Nanaimo'], data['Pemberton Valley'], data['Port Alberni'],
                           data['Port Edward'], data['Powell River'], data['Prince George'], 
                           data['Prince Rupert'], data['Quesnel'], data['Revelstoke'],
                           data['Salt Spring Island'], data['Shuswap'], data['Skeena'], 
                           data['Smithers'], data['South Okanagan Similkameen'],
                           data['Squamish'], data['Sunshine Coast'], data['Terrace'], 
                           data['Vernon'], data['Victoria'], data['West Kootenay'], 
                           data['Whistler'], data['Williams Lake'])
    # Save or print output
    if not os.path.exists(CWD + OUTPUT_DIR):
        os.mkdir(CWD + OUTPUT_DIR)
    file = open(CWD+OUTPUT_DIR+f'{string.lower()}_anova_result.txt', 'w')
    file.write(f'{string.replace("_", " ")} AVOVA result: {anova}')
    file.close()
    return anova.pvalue

# Function performs pairwise Tukey-U analysis on a given melted dataset
def performPostHocAnalysis(m_data, string):
     print(f' - Preforming Posthoc Analysis on {string.replace("_", " ")}')
     posthoc = pairwise_tukeyhsd(m_data['value'], m_data['variable'], alpha=0.05)
     figure = posthoc.plot_simultaneous(xlabel=f'Sampled Mean {string.replace("_", " ")}',
                                     ylabel='city', figsize=(20, 15))
     
     # Check if there is an output director and save csv file to it
     if not os.path.exists(CWD + OUTPUT_DIR):
         os.mkdir(CWD + OUTPUT_DIR)
     plt.savefig(CWD+OUTPUT_DIR+f'{string.lower()}_tukey_u_simultaneous_plot.png')
     temp = pd.DataFrame(data=posthoc._results_table.data[1:], 
                       columns=posthoc._results_table.data[0])
     temp.to_csv(CWD+OUTPUT_DIR+f'{string.lower()}_pairwise_tukeyhsd_result.txt')

# Function to perform a linear regression between to presumed non-independent sets of data
def performLinearRegression(data1, data2, string):
    print(f' - Performing linear regression on {string.replace("_", " ")}')
    regression = stats.linregress(data1['value'], data2['value'])
    x_range = np.linspace(0, 100, 50)
    prediction = x_range * regression.slope + regression.intercept
    plot = plt.figure(figsize=(15, 12))
    plt.scatter(data1['value'], data2['value'], alpha=0.5, label='Distances vs Avg Speeds')
    plt.plot(x_range, prediction, 'r-', alpha=0.5, label='Linear Regression')
    plt.plot([], [], ' ', label=f'Correlation Coefficient r = {regression.rvalue}, r^2 = {regression.rvalue**2}')
    plt.title('Linear Reagression of Distance Traveled and Avg Speed ')
    plt.xlabel('Sampled Mean Distances (km)')
    plt.ylabel('Sampled Avg Speeds (km/hr)')
    plt.legend()

    if not os.path.exists(CWD + OUTPUT_DIR):
        os.mkdir(CWD + OUTPUT_DIR)
    plt.savefig(CWD + OUTPUT_DIR + f'{string.lower()}_linear_regression.png')

# Main function 
def main():
    print('Please wait while the analysis is performed...')
    # Read in files
    dist_data = pd.read_csv(CWD + SAMPLES_DIR + 'sampled_dist_data.csv')
    speed_data = pd.read_csv(CWD + SAMPLES_DIR + 'sampled_speed_data.csv')
    createHistograms(dist_data, DIST_STRING)
    createHistograms(speed_data, SPEED_STRING)
    melted_dist_data = pd.DataFrame()
    melted_speed_data = pd.DataFrame()

    # If ANOVA test passes move on to Tukey-U test
    if performAnova(dist_data, DIST_STRING) < 0.05:
        print(f' - ANOVA p-value < 0.05 for {DIST_STRING.replace("_", " ")}, '
              + 'we can conclude there is a difference between means of the city distances')
        melted_dist_data = pd.melt(dist_data)
        performPostHocAnalysis(melted_dist_data, DIST_STRING)
    else:
        print(f'Because ANOVA p-value > 0.05 for {DIST_STRING.replace("_", " ")}, '
              + 'we cannot conclude there is a difference between means of the city distances')
    if performAnova(speed_data, SPEED_STRING) < 0.05:
        print(f' - ANOVA p-value < 0.05 for {SPEED_STRING.replace("_", " ")}, '
              + 'we can conclude there is a difference between means of the city distances')
        melted_speed_data = pd.melt(speed_data)
        performPostHocAnalysis(melted_speed_data, SPEED_STRING)   
    else:
        print(f'Because ANOVA p-value > 0.05 for {SPEED_STRING.replace("_", " ")}, '
              + 'we cannot conclude there is a difference between means of the city distances')
        
    performLinearRegression(melted_dist_data, melted_speed_data, 'Distance_and_Speed')
    
    print(f'Finished, output filed saved to {OUTPUT_DIR}')
    
if __name__ == '__main__':
    main()