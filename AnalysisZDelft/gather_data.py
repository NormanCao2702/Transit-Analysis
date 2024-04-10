# CMPT 353 PROJECT
# Zachariah Delft, 301386141

# Transit-Analysis

# Gather Data
# Program is meant to do the following
# [1] Opens each CSV text file and puts data into pandas dataframe
# [2] Gets city from file name
# [3] Create dataframes of sampled distances traveled and avg speeds
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
    return city.group(0).replace('_', ' ')

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

# function to get time difference in hours
def getHrs(diff):
    days = diff.days
    seconds = diff.seconds
    return (days * 24) + (seconds / 3600)
getHrs = np.vectorize(getHrs, otypes=[np.float64])

# Main function
def main():
    print('Please wait while data is cleaned and saved to a more usable form...')
    # from the data with cities as column names
    sampled_dist_data = pd.DataFrame()
    sampled_speed_data = pd.DataFrame()
    # Iterate files
    for file in os.listdir(CWD + STOP_TIME_DIR):
        # Get city name from filename
        city = getCity(file)
        print(f' - Cleaning and Re-organizing Data for {city}')
        # Get data from csv and put into pandas dataframe
        temp_timing = pd.read_csv(CWD+STOP_TIME_DIR+file)
        # A series of samples used later for ANOVA test and tukey-u (per city)
        dist_samples = pd.Series()
        speed_samples = pd.Series()
        # Add city name as column
        temp_timing['city'] = city
        # Fix data in greater_vancouver files
        temp_timing['shape_dist_traveled'] = temp_timing['shape_dist_traveled'].replace(np.nan, 0)
        if city != 'Greater Vancouver':
            temp_timing['shape_dist_traveled'] = temp_timing['shape_dist_traveled'] / 1000 # km
        # Turn column 'arrival_time' to datetime object
        temp_timing['arrival_time'] = getTime(temp_timing['arrival_time'])
        temp_timing['departure_time'] = getTime(temp_timing['departure_time'])
        
        # Get only rows with routw beginnig
        temp_beginning = temp_timing.loc[temp_timing.groupby(['trip_id'])['shape_dist_traveled'].idxmin()]
        # Remove unneeded column
        temp_beginning = temp_beginning.drop(columns=['arrival_time'])
        temp_beginning = temp_beginning.drop(columns=['shape_dist_traveled'])
        # Get only rows with route endings
        temp_end = temp_timing.loc[temp_timing.groupby(['trip_id'])['shape_dist_traveled'].idxmax()]
        # Remove unneeded column
        temp_end = temp_end.drop(columns=['departure_time'])
        # Merge needed information into single dataFrame
        temp_dist = temp_beginning.merge(temp_end[['arrival_time', 'trip_id', 'shape_dist_traveled']], 
                                         how='inner', on='trip_id')
        # Sort for visual checks - remove at later time
        temp_dist = temp_dist.sort_values(['trip_id'], ignore_index=True)
        
        # Find time difference between start and end of route
        temp_dist['time_diff'] = temp_dist['arrival_time'] - temp_dist['departure_time']
        # Convert Difference to hours
        temp_dist['time_diff'] = getHrs(temp_dist['time_diff'])
        # Calculate average speed drivers need to sustain to meet deadline
        temp_dist['avg_speed'] = temp_dist['shape_dist_traveled'] / temp_dist['time_diff']
        
        # Create samples
        for i in range(61):
            sample = temp_dist.sample(n=2, replace=False)
            # Distances (km)
            dist_mean = sample.loc[:, 'shape_dist_traveled'].mean()
            dist_samples = pd.concat([dist_samples, pd.Series([dist_mean])], ignore_index=True)
            # Speeds (km/h)
            speed_mean = sample.loc[:, 'avg_speed'].mean()
            speed_samples = pd.concat([speed_samples, pd.Series([speed_mean])])
        sampled_dist_data[city] = dist_samples
        sampled_speed_data[city] = speed_samples
        
        
    # Check if there is an output director and save csv file to it
    if not os.path.exists(CWD + OUTPUT_DIR):
        os.mkdir(CWD + OUTPUT_DIR)
    sampled_dist_data.to_csv(CWD + OUTPUT_DIR + 'sampled_dist_data.csv', index=False)
    sampled_speed_data.to_csv(CWD + OUTPUT_DIR + 'sampled_speed_data.csv', index=False)
    
    print('...Finished cleaning data')


if __name__ == '__main__':
    main()