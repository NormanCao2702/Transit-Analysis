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

SAMPLES_DIR = '\\gathered_data\\'
CWD = os.getcwd()

def main():
    # Read in file
    data = pd.read_csv(CWD + SAMPLES_DIR + 'sampled_data.csv')
    print(data)
    
    # Create and save histogram of the samples
    
    
if __name__ == '__main__':
    main()