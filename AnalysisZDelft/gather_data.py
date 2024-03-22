# CMPT 353 PROJECT
# Zachariah Delft, 301386141
#
#

# Gather Data

import requests
import csv
from datetime import date

# Text file where key is saved
KEY_FILE = 'transit_api_key.txt'
# API endpoint
API_URL = 'https://external.transitapp.com/v3/otp/plan'
# file csv is saved to
OUT_FILE = 'transit_route.csv'
# Latitudes and longitudes for SFU and a chosen "home" location
SFU_LATLONG = '49.2781, 122.9199'
HOME_LATLONG = '49.2328, 123.0661'
# Variables to hold start times and finish times (UTC)
HR, MIN = 12, 0
# Date for request
DATE = date.today()

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
    
    # Get file ready for writing
    file = open(OUT_FILE, mode='a', newline='', encoding='utf-8')
    while HR != 8 & MIN != 30:
        responses = requests.get(API_URL, 
                                 headers = {'apikey': API_KEY, 
                                            'Accept-Language': 'en'},
                                 params = {'fromPlace': HOME_LATLONG, 
                                           'toPlace': SFU_LATLONG,
                                           'date': f'{DATE.year}-{DATE.month}-{DATE.day + 1}',
                                           'time': f'{HR}:{MIN}'})
        if responses.status_code == 200:
            data = responses.json()
    

if __name__ == '__main__':
    main()