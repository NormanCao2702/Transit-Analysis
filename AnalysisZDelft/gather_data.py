# CMPT 353 PROJECT
# Zachariah Delft, 301386141
#
#

# Gather Data

import requests
import csv
from datetime import datetime, time, timedelta

# Text file where key is saved
KEY_FILE = 'transit_api_key.txt'
# API endpoint
API_URL = 'https://external.transitapp.com/v3/otp/plan'
# file csv is saved to
OUT_FILE = 'transit_route.csv'
# Latitudes and longitudes for SFU and a chosen "home" location
SFU_LATLONG = 'SFU::49.2781,122.9199'
HOME_LATLONG = 'HOME::49.2328,123.0661'

# Function to get transit API key from text file
def getAPIKey():
    file = open(KEY_FILE, 'r')
    key = file.read().rstrip()
    file.close()
    return key

# Main function
def main():
    # Get API key and request information
    API_KEY = getAPIKey()
    
    # Time must be in UTC
    DATE = datetime.combine(datetime.now().date(), time(12, 0)) #+ timedelta(days=1)
    END_DATE = DATE + timedelta(days=1)
    print(f"{DATE}")
    
    # Get file ready for writing
    file = open(OUT_FILE, mode='w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    # Write header for CSV file
    headers = {'apikey': API_KEY, 'Accept-Language': 'en'}
    params = {'fromPlace': HOME_LATLONG,
              'toPlace': SFU_LATLONG,
              'date': f'{DATE.date()}',
              'time': f'{DATE.hour}:{DATE.minute}'}
    
    responses = requests.get(API_URL, headers=headers, params = params)
    
    if responses.status_code == 200:
        data = responses.json()
        plan = data['plan']
        print(len(plan['itineraries']))
        for itinerarie in plan['itineraries']:
            print(itinerarie)
    else:
        print('fail')
    
   
    

if __name__ == '__main__':
    main()