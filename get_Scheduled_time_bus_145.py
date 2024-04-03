#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 1 Identify Route ID for Bus 145
# 2 Determine Trip IDs for Both Directions


# In[2]:


import pandas as pd


# In[3]:


def routeID():
    # Load the routes.txt file
    routes_df = pd.read_csv('GTFS-Static-Data/routes.txt')

    # Search for Bus 145 in either the route_short_name or route_long_name columns
    bus_145_filter = routes_df['route_short_name'].str.contains('145', na=False) | routes_df['route_long_name'].str.contains('145', na=False)

    # Filter for rows that mention '145', which might indicate Bus 145's route
    bus_145_routes = routes_df[bus_145_filter]
    bus_145_id = bus_145_routes['route_id'].iloc[0]
    
    # Display the filtered DataFrame to identify the Route ID(s) for Bus 145
#     print(bus_145_routes[['route_id', 'route_short_name', 'route_long_name']])
    return bus_145_id


# In[4]:


def tripID(route_id):
    # Load the trips.txt file
    trips_df = pd.read_csv('GTFS-Static-Data/trips.txt')

    # Filter for trips that belong to the given route ID
    bus_145_trips = trips_df[trips_df['route_id'] == route_id]

    # Separate the trips by direction
    trips_direction_0 = bus_145_trips[bus_145_trips['direction_id'] == 0]['trip_id'].tolist()
    trips_direction_1 = bus_145_trips[bus_145_trips['direction_id'] == 1]['trip_id'].tolist()

    return trips_direction_0, trips_direction_1


# In[5]:


def stopID(stop_name):
    # Load the stops.txt file
    stops_df = pd.read_csv('GTFS-Static-Data/stops.txt')

    # Filter stops containing the specified keywords in their names
    filtered_stops = stops_df[stops_df['stop_name'].str.contains('|'.join(stop_name), case=False, na=False)]

    return filtered_stops[['stop_id', 'stop_name']]


# In[6]:


def getScheduledTimes(trip_ids, origin_stop_id, destination_stop_id):
    # Load the stop_times.txt file
    stop_times_df = pd.read_csv('GTFS-Static-Data/stop_times.txt')

    # Filter for the relevant trips
    relevant_trips = stop_times_df[stop_times_df['trip_id'].isin(trip_ids)]

    # Further filter for only the origin and destination stops
    origin_times = relevant_trips[relevant_trips['stop_id'] == origin_stop_id]
    destination_times = relevant_trips[relevant_trips['stop_id'] == destination_stop_id]

    # Create a DataFrame to hold the scheduled times for each trip at the origin and destination
    scheduled_times = pd.DataFrame({
        'trip_id': trip_ids,
        'origin_scheduled_time': [origin_times[origin_times['trip_id'] == trip_id]['arrival_time'].values[0] for trip_id in trip_ids],
        'destination_scheduled_time': [destination_times[destination_times['trip_id'] == trip_id]['arrival_time'].values[0] for trip_id in trip_ids]
    })

    return scheduled_times


# In[7]:


def main():
    route_id_for_145 = routeID()
    # trip_dir 0 = Pro to SFu, trip_dir 1 = SFU to Pro
    trips_direction_0, trips_direction_1 = tripID(route_id_for_145)
    
#     print(f"Trip IDs for Bus 145 from Production Way to SFU (Direction 0): {trips_direction_0}")
#     print(f"Trip IDs for Bus 145 from SFU to Production Way (Direction 1): {trips_direction_1}")
    # Find stop IDs for Production Way
    
    production_way_stop = stopID(['Production Way Station @ Bay 1'])
    production_way_stop_id = production_way_stop['stop_id'].iloc[0]
    print(production_way_stop)
    print(f"Production way stop id: {production_way_stop_id}")

    # Find stop IDs for SFU & production way
    sfu_stop = stopID(['SFU Transit Exchange @ Bay 1'])
    sfu_stop_id = sfu_stop['stop_id'].iloc[0]
#     print(sfu_stop)
#     print(f"SFU Stop id: {sfu_stop_id}")
    pro_to_sfu_scheduled_times = getScheduledTimes(trips_direction_0, production_way_stop_id, sfu_stop_id)
    sfu_to_pro_scheduled_times = getScheduledTimes(trips_direction_1, sfu_stop_id, production_way_stop_id)

    pro_to_sfu_scheduled_times.to_csv("Production Way Bay 1 to SFU Bay 1 scheduled time.csv", index=False)
    sfu_to_pro_scheduled_times.to_csv("SFU Bay 1 to Production Way Bay 1 scheduled time.csv", index=False)
    
#     print(pro_to_sfu_scheduled_times)
#     print(sfu_to_pro_scheduled_times)


# In[8]:


main()

