# CMPT 353 PROJECT
# Zachariah Delft, 301386141

# Transit-Analysis

# perform_anova_tukey.py
# Program is meant to do the following
# [1] open sample_data.csv into a pandas dataframe
# [2] Create a histogram of the samples
# [3] Perform ANOVA test on data by column = city
# [4] Perform a one-sided t-test 

import os
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

SAMPLES_DIR = '\\gathered_data\\'
OUTPUT_DIR = '\\analysis_results\\'
CWD = os.getcwd()

def createHistograms(data):
    # Create and save histogram of the samples
    # Made reference to:
    # https://matplotlib.org/stable/gallery/statistics/histogram_multihist.html
    figure, axis = plt.subplots(nrows=4, ncols=2)
    figure.suptitle('Histogram of Mean Sampled Max Distances')
    figure.set_figheight(15)
    figure.set_figwidth(15)
    figure.tight_layout()
    i = 0
    j = i + 6
    x, y = 0, 0
    while j <= 48:
        if j > 46:
            j = 45
        axis[y, x].hist(data.iloc[:,i:j], bins=20, alpha=0.5)
        axis[y, x].legend(data.iloc[:,i:j].columns, prop={'size':10})
        y = (y+1)
        if y == 4:
            y = 0
            x = 1
        i = i + 6
        j = j + 6
        if not os.path.exists(CWD + OUTPUT_DIR):
            os.mkdir(CWD + OUTPUT_DIR)
        plt.savefig(CWD+OUTPUT_DIR+'distance_histograms.png')

def performAnova(data):
    anova = stats.f_oneway(data['100_mile_house'], data['Agassiz-Harrison'], 
                           data['Ashcroft_Cache_Creek_Clinton'], data['Bulkley_Nechako'], 
                           data['Campbell_River'], data['Central_Fraser_Valley'], 
                           data['Chilliwack'], data['Clearwater'], data['Columbia_Valley'], 
                           data['Comox_Valley'], data['Cowichan_Valley'], data['Cranbrook'], 
                           data['Creston_Valley'], data['Dawson_Creek'], data['Elk_Valley'], 
                           data['Fort_St_John'], data['Greater_Vancouver'], data['Hazeltons'], 
                           data['Hope'], data['Kamloops'], data['Kelowna'], data['Kimberley'], 
                           data['Kitimat'], data['Merritt'], data['Mount_Waddington'], 
                           data['Nanaimo'], data['Pemberton_Valley'], data['Port_Alberni'],
                           data['Port_Edward'], data['Powell_River'], data['Prince_George'], 
                           data['Prince_Rupert'], data['Quesnel'], data['Revelstoke'],
                           data['Salt_Spring_Island'], data['Shuswap'], data['Skeena'], 
                           data['Smithers'], data['South_Okanagan_Similkameen'],
                           data['Squamish'], data['Sunshine_Coast'], data['Terrace'], 
                           data['Vernon'], data['Victoria'], data['West_Kootenay'], 
                           data['Whistler'], data['Williams_Lake'])
    # Save or print output
    if not os.path.exists(CWD + OUTPUT_DIR):
        os.mkdir(CWD + OUTPUT_DIR)
    file = open(CWD+OUTPUT_DIR+'anova_result.txt', 'w')
    file.write(f'AVOVA result: {anova}')
    file.close()
    print(f'AVOVA result: {anova}')
    return anova.pvalue

def performPostHocAnalysis(m_data):
     posthoc = pairwise_tukeyhsd(m_data['value'], m_data['variable'], alpha=0.05)
     figure = posthoc.plot_simultaneous(xlabel='Sampled Mean Max Distances',
                                     ylabel='city', figsize=(20, 15))
     
     # Check if there is an output director and save csv file to it
     if not os.path.exists(CWD + OUTPUT_DIR):
         os.mkdir(CWD + OUTPUT_DIR)
     plt.savefig(CWD+OUTPUT_DIR+'tukey_u_simultaneous_plot.png')
     # Made reference to:
     # https://stackoverflow.com/questions/40516810/saving-statmodels-tukey-hsd-into-a-python-pandas-dataframe
     temp = pd.DataFrame(data=posthoc._results_table.data[1:], 
                       columns=posthoc._results_table.data[0])
     temp.to_csv(CWD+OUTPUT_DIR+'pairwise_tukeyhsd_result.txt')
     print(posthoc)

def main():
    # Read in file
    data = pd.read_csv(CWD + SAMPLES_DIR + 'sampled_data.csv')
    createHistograms(data)
    
    # Perform ANOVA test
    column_list = []
    column_names = data.columns.values.tolist()
    for name in column_names:
        column_list.append(data[name])
    
    # If ANOVA test passes move on to Tukey-U test
    
    if performAnova(data) < 0.05:
        melted_data = pd.melt(data)
        performPostHocAnalysis(melted_data)
        
    else:
        print(f'Because ANOVA p-value > 0.05, we cannot conclude there '
              + 'is a difference between means of the city distances')
    
    
if __name__ == '__main__':
    main()