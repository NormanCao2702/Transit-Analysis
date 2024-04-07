# Libraries
import requests
from datetime import datetime
import json
import threading
import time
from multiprocessing import Lock


# Contant Variables
# API Keys
TESTING_API_KEY = '8RNVMZ3pgYCOlTMIWqRy'
API_KEYS = [TESTING_API_KEY, TESTING_API_KEY, TESTING_API_KEY]

# URLs
TRANSLINK_BUSES_URL = 'https://api.translink.ca/rttiapi/v1/buses'

# Bus Data
ROUTE_NUMBERS = ['R5', '144', '145']

# Directories
REAL_TIME_DATA_DIRECTORY = 'real_time_data/'


# Global Variables
lock = Lock()


# Print the message in multithreading
def printMessageInMultithreading(message):
    lock.acquire()
    try:
        print(message)
    finally:
        lock.release()


# Get the real time data and write to file
def getRealTimeDataAndWrite(index):
    # Get the current time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate the file name
    file_name = ROUTE_NUMBERS[index] + '_' + current_time + '.json'
    file_location = REAL_TIME_DATA_DIRECTORY + file_name
    printMessageInMultithreading(file_name)
    
    # HTTP GET parameters
    params = {
        'apikey': API_KEYS[index],
        'routeNo': ROUTE_NUMBERS[index]
    }

    # HTTP GET headers
    headers = {
        'accept': 'application/JSON'
    }

    # Send a HTTP GET request
    http_get_data = requests.get(TRANSLINK_BUSES_URL, params=params, headers=headers)
    
    # Write to file
    with open(file_location, 'w') as f:
        json.dump(http_get_data.json(), f, indent=4)


# Get all the real time data
def getAllRealTimeData():
    for idx, _ in enumerate(ROUTE_NUMBERS):
        threading.Thread(target=getRealTimeDataAndWrite, args=(idx, )).start()


# Run every minute
def runEveryMinute():
    while True:
        getAllRealTimeData()
        time.sleep(60)


if __name__ == '__main__':
    runEveryMinute()
