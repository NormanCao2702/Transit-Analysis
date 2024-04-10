# Libraries
import os
import pandas as pd
import json


# Constant Variables
# Directories
REAL_TIME_DATA_DIRECTORY = 'real_time_data/'

# Filenames
EXTRACTED_REAL_TIME_DATA_FILENAME = 'extracted_real_time_data.json'
EXTRACTION_REPORT = 'extraction_report.json'


# Extract the real time data and write to file
def extractRealTimeDataAndWrite():
    extraction_report = {
        'data_count': 0,
        'file_count': 0,
        'valid_file_count': 0,
        'invalid_file_count': 0,
        'invalid_filenames': []
    }
    
    # Get all the filenames
    filenames = os.listdir(REAL_TIME_DATA_DIRECTORY)
    extraction_report['file_count'] = len(filenames)
    
    # Loop for reading each file
    df_list = []
    for filename in filenames:
        print('Reading the file: ' + filename)
        try:
            df = pd.read_json(REAL_TIME_DATA_DIRECTORY + filename)
            df_list.append(df)
            extraction_report['valid_file_count'] += 1
        except:
            extraction_report['invalid_filenames'].append(filename)
            extraction_report['invalid_file_count'] += 1
        
    # Concat all the data frames into one data frame
    df = pd.concat(df_list)
    extraction_report['data_count'] = df.shape[0]
    
    # Save the data frame into a json file
    df.to_json(EXTRACTED_REAL_TIME_DATA_FILENAME, orient='records')
    
    # Save the extraction report
    print('Writing the extraction report: ' + EXTRACTION_REPORT)
    with open(EXTRACTION_REPORT, 'w') as f:
        json.dump(extraction_report, f, indent=4)


if __name__ == '__main__':
    extractRealTimeDataAndWrite()
