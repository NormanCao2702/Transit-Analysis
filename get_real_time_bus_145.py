#!/usr/bin/env python
# coding: utf-8

# In[104]:


import requests
import time
import pandas as pd
from datetime import datetime
import pytz


# In[46]:


# Your API key for authorization
api_key = 'bf26424bdabada8b6cb6769478a36213bd864f1773e7a3ac5ecfc15ef83830ce'
# Header parameters
headers = {
    'apiKey': api_key,  # Authorization with API key
    'Accept-Language': 'en'  # Optional: Language preference
}


# In[47]:


# Getting Production way bay 1 global stop id
production_way_bay_1_stop = None


# In[71]:


def connecting_endpoint():
    # API endpoint for nearby stops
    nearby_stops_url= "https://external.transitapp.com/v3/public/nearby_stops"
    # Query parameters
    params_nearby_stops = {
        'lat': 49.25348197787918,  # Latitude
        'lon': -122.91818244659417,  # Longitude
        'max_distance': 150,  # Maximum radius of search from the request location in meters
        'stop_filter': 'Routable',  # Type of stops to return
        # Optional: you can add 'pickup_dropoff_filter' parameter here if needed
    }
    # Make the GET request
    response_nearby = requests.get(nearby_stops_url, params=params_nearby_stops, headers=headers)
    return response_nearby


# In[80]:


def get_stop_global_id(response_nearby, desired_stop_name):
    # Check if the request was successful
    if response_nearby.status_code == 200:
        data = response_nearby.json()

        stops = data['stops']

        # Loop through each stop in the response and print its global_stop_id
#         for stop in stops:
#             print(f"Stop Name: {stop['stop_name']}, Global Stop ID: {stop['global_stop_id']}")

        # Desired stop name
#         stop_name = "Production Way Station (Bay 1)"
        for stop in stops:
            if stop["stop_name"] == desired_stop_name:
#                 production_way_bay_1_stop = stop["global_stop_id"]
                return stop["global_stop_id"]
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")


# In[89]:


def get_current_time():
    return int(time.time())


# In[90]:


def fetch_stop_departures(global_stop_id, current_time):
    stop_departures_url = "https://external.transitapp.com/v3/public/stop_departures"

    # Query parameters
    params_stop_departures = {
        'global_stop_id': global_stop_id,
        'time': current_time,  # You can adjust this according to your needs
        'should_update_realtime': True,
        'remove_cancelled': False # Set to True if you want to remove cancelled schedule items
    }

    # Make the GET request
    response_stop_depart = requests.get(stop_departures_url, params=params_stop_departures, headers=headers)
    return response_stop_depart


# In[91]:


def process_stop_departures(response):
    if response.status_code == 200:
        data = response.json()
        departures = []
        # Extracting data
        for route_departure in data['route_departures']:
            for itinerary in route_departure['itineraries']:
                for schedule_item in itinerary['schedule_items']:
                    departure_info = {
                        'RT_Trip_ID': schedule_item['rt_trip_id'],
                        'Departure_Time': schedule_item['departure_time'],
                        'Scheduled_Departure_Time': schedule_item['scheduled_departure_time'],
                        'Is_Cancelled': schedule_item['is_cancelled']
                    }
                    departures.append(departure_info)
                    print(f"RT Trip ID: {schedule_item['rt_trip_id']}, Departure Time: {schedule_item['departure_time']}, Scheduled Departure Time: {schedule_item['scheduled_departure_time']}, Is cancelled: {schedule_item['is_cancelled']}")
        return departures
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None


# In[130]:


def update_or_append_departures(departures_df, csv_file='departures_info.csv'):
    try:
        existing_df = pd.read_csv(csv_file, dtype={'RT_Trip_ID': str})
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=departures_df.columns)

    # Ensure RT_Trip_ID is a string to avoid comparison issues
    departures_df['RT_Trip_ID'] = departures_df['RT_Trip_ID'].astype(str)

    updated_df = pd.DataFrame()  # Initialize an empty DataFrame to hold updated rows

    for index, new_row in departures_df.iterrows():
        trip_id = new_row['RT_Trip_ID']
        
        if trip_id in existing_df['RT_Trip_ID'].values:
            # Filter out the old row with the same trip_id
            existing_df = existing_df[existing_df['RT_Trip_ID'] != trip_id]
        
        # Append new_row to updated_df (whether it was in existing_df or not)
        updated_df = pd.concat([updated_df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Concatenate the remaining existing_df rows with the updated/added rows
    final_df = pd.concat([existing_df, updated_df], ignore_index=True)
    
    # Write the final DataFrame back to the CSV file
    final_df.to_csv(csv_file, index=False)


# In[133]:


def main():
    # Desired stop name
    desired_stop_name = "Production Way Station (Bay 1)"

#     response_nearby = connecting_endpoint()
#     production_way_bay_1_stop = get_stop_global_id(response_nearby, desired_stop_name)
    
#     if production_way_bay_1_stop:
#         print(f"Global Stop ID for '{desired_stop_name}': {production_way_bay_1_stop}")
#     else:
#         print(f"Stop '{desired_stop_name}' not found.")
    
    production_way_bay_1_stop = "TSL:74401"
    
    current_time = get_current_time()
    response = fetch_stop_departures(production_way_bay_1_stop, current_time)
    
    departures = process_stop_departures(response)
    departures_df = pd.DataFrame(departures)
    
    # Define the timezone for Vancouver
    vancouver_tz = pytz.timezone('America/Vancouver')
    # Convert UNIX time to datetime objects in UTC, then convert to Vancouver timezone
    departures_df['Departure_Time'] = pd.to_datetime(departures_df['Departure_Time'], unit='s').dt.tz_localize('UTC').dt.tz_convert(vancouver_tz)
    departures_df['Scheduled_Departure_Time'] = pd.to_datetime(departures_df['Scheduled_Departure_Time'], unit='s').dt.tz_localize('UTC').dt.tz_convert(vancouver_tz)

    # Extract just the time part, post conversion
    departures_df['Departure_Time'] = departures_df['Departure_Time'].dt.time
    departures_df['Scheduled_Departure_Time'] = departures_df['Scheduled_Departure_Time'].dt.time
    
    # Append to CSV, checking if the file exists to handle headers
    update_or_append_departures(departures_df)
    
    # Display the updated DataFrame
    print(departures_df)


# In[135]:


# if __name__ == "__main__":
main()

