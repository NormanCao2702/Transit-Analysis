# CMPT 353 PROJECT
# Zachariah Delft, 301386141

# Transit-Analysis

# Gather Data
# Program is meant to do the following
# [1] Opens each CSV text file and puts data into pandas dataframe
# [2] Add city/transit jurisdiction name column
# [3] 
# [4] Save wanted/more usable data to a csv file in an output directory
# Data files in 'city_stop_data_files' was manually downloaded from the 
# following sources, and partly seperated for storage needs:
# - https://www.bctransit.com/open-data/
# - https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/gtfs/gtfs-data

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Directories holding raw data
STOP_TIME_DIR = '\\city_stop_data_files\\stop_times\\'
STOP_INFO_DIR = '\\city_stop_data_files\\stop_info\\'
OUTPUT_DIR = '\\gathered_data\\'
CWD = os.getcwd()

# Function used to calculate the schedualed wait times between departures at 
# stops. Returns time difference if next stop id and trip id is the same as 
# current
def calcWaitTime(nextTime, curTime):#, nextTrip, curTrip):
    
    diff = nextTime - curTime
    return diff.total_seconds()
    return np.NaN
calcWaitTime = np.vectorize(calcWaitTime, otypes=[np.float64])

# Following regular expression and function return the city name as a string
# for a given file name
regex = re.compile('(.+?)(?=_stop)')
def getCity(filename):
    city = regex.search(filename)
    return city.group(0)

# Function used to conver string to hr, min, sec datetime
def getTime(string):
    timeSubStr = re.findall('\d+', string)
    hr, minute, sec = timeSubStr
    addDays = 0
    if int(hr) >= 24:
        addDays = 1
        hr = f'{int(hr) - 24}'
    time = datetime.strptime(f'{hr}:{minute}:{sec}', '%H:%M:%S')
    time = time + timedelta(days=addDays)
    return time
getTime = np.vectorize(getTime, otypes=[np.datetime64])

# Main function
def main():
    
    # initializing pandas dataframe
    stop_timing = pd.DataFrame()
    stop_info = pd.DataFrame()
    # Iterate files
    for file in os.listdir(CWD + STOP_TIME_DIR):
        # Get city name from filename
        city = getCity(file)
        # Get data from csv and put into pandas dataframe
        temp_timing = pd.read_csv(CWD+STOP_TIME_DIR+file)
        # Add city name as column
        temp_timing['city'] = city
        # Fix data in greater_vancouver files
        if city == 'Greater_Vancouver':
            temp_timing['shape_dist_traveled'] = temp_timing['shape_dist_traveled'].replace(np.nan, 0)
            temp_timing['shape_dist_traveled'] = temp_timing['shape_dist_traveled'] * 1000
        # Append to bigger pandas dataframe
        stop_timing = pd.concat([stop_timing, temp_timing], ignore_index=True)
    for file in os.listdir(CWD + STOP_INFO_DIR):
        # Get data from csv and put into pandas dataframe
        temp_info = pd.read_csv(CWD+STOP_INFO_DIR+file)
        # Append to bigger pandas dataframe
        stop_info = pd.concat([stop_info, temp_info], ignore_index=True)
    # Join newly formed dataframes by stop_id    
    data = stop_timing.merge(stop_info, how='inner', on='stop_id')
    data = data.dropna(axis='columns')
    data = data.sort_values(['city', 'trip_id', 'stop_sequence'], ignore_index=True)
    print(data)
            
    # Check if there is an output director and save csv file to it
    if not os.path.exists(CWD + OUTPUT_DIR):
        os.mkdir(CWD + OUTPUT_DIR)
    data.to_csv(CWD + OUTPUT_DIR + 'city_wait_times.csv', index=False)
    
      

if __name__ == '__main__':
    main()