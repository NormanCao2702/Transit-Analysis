# CMPT 353 PROJECT
# Zachariah Delft, 301386141

# Transit-Analysis

# Gather Data
# Program is meant to do the following
# [1] Opens each CSV text file and puts data into pandas dataframe
# [2] Add city/transit jurisdiction name column
# [3] Calculate schedualed wait times for stops dependent on route 
# [4] Save wanted more usable data to a csv file in an output directory
# Data files in 'city_stop_data_files' was manually downloaded from the 
# following sources, and manually seperated for storage needs:
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
def calcWaitTime(nextTime, curTime, nextStop, curStop):#, nextTrip, curTrip):
    if nextStop == curStop:# and nextTrip == curTrip:
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
    # Iterate files
    for file in os.listdir(CWD + STOP_TIME_DIR):
        city = getCity(file)
        print(city)
        init_data = pd.read_csv(CWD+STOP_TIME_DIR+file)
        init_data['city'] = city
        init_data['arrival_time'] = getTime(init_data['arrival_time'])
        init_data = init_data.sort_values(by=['stop_id', 'arrival_time'], 
                                          ignore_index=True)
        init_data['next_time'] = init_data['arrival_time'].shift(-1)
        init_data['next_sid'] = init_data['stop_id'].shift(-1)
        init_data['next_tid'] = init_data['trip_id'].shift(-1)
        
        init_data['wait_time'] = calcWaitTime(init_data['next_time'],
                                              init_data['arrival_time'],
                                              init_data['next_sid'],
                                              init_data['stop_id'],
                                              #init_data['next_tid'],
                                              #init_data['trip_id']
                                              )
        
        if not os.path.exists(CWD + OUTPUT_DIR):
            os.mkdir(CWD + OUTPUT_DIR)
        init_data.to_csv(CWD + OUTPUT_DIR + f'{city}.csv', 
                         columns={'city', 'stop_id', 'trip_id', 
                                  'arrival_time', 'next_time', 
                                  'wait_time', 'next_sid', 'next_tid'})
      

if __name__ == '__main__':
    main()