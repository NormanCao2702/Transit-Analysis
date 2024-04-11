import pandas as pd

def filter_by_route(routes_df, route_short_name):
    """
    Filters routes DataFrame by short name and returns the route ID.

    Parameters:
    - routes_df: DataFrame containing route data.
    - route_short_name: The short name of the route to filter by.

    Returns:
    - The route ID matching the given short name.
    """
    return routes_df[routes_df['route_short_name'] == route_short_name]['route_id'].iloc[0]

def filter_by_stop(stops_df, stop_name):
    """
    Filters stops DataFrame by stop name and returns the stop ID.

    Parameters:
    - stops_df: DataFrame containing stop data.
    - stop_name: The name of the stop to filter by, case insensitive.

    Returns:
    - The stop ID of the first stop matching the given name.
    """
    return stops_df[stops_df['stop_name'].str.contains(stop_name, case=False, na=False)]['stop_id'].iloc[0]

def filter_trips_by_route_and_direction(trips_df, route_id, direction_id):
    """
    Filters trips DataFrame by route ID and direction.

    Parameters:
    - trips_df: DataFrame containing trip data.
    - route_id: The ID of the route to filter by.
    - direction_id: The direction of the trip to filter by.

    Returns:
    - A filtered DataFrame with trips matching the given route ID and direction.
    """
    return trips_df[(trips_df['route_id'] == route_id) & (direction_id == direction_id)]

def filter_stop_times_by_trip_and_stop(stop_times_df, trips_df, stop_id):
    """
    Filters stop times DataFrame by trip ID and stop ID.

    Parameters:
    - stop_times_df: DataFrame containing stop time data.
    - trips_df: DataFrame containing filtered trip data.
    - stop_id: The ID of the stop to filter by.

    Returns:
    - A filtered DataFrame with stop times for the specified trip and stop.
    """
    # merged_df = pd.merge(stop_times_df, trips_df, on='trip_id')
    # merged_df.to_csv("temp.csv")
    # merged_df =merged_df[merged_df['stop_id'] == stop_id]
    # print(merged_df)
    # return merged_df[merged_df['stop_id'] == stop_id]
    merged_df = pd.merge(stop_times_df, trips_df, on='trip_id')
    filtered_df = merged_df[merged_df['stop_id']==stop_id]
    return filtered_df

def get_trips_by_day(trip_df, calendar_df, day_name):
    """
    Filters trips by day of the week.

    Parameters:
    - trip_df: DataFrame containing trip data.
    - calendar_df: DataFrame containing calendar data for service schedules.
    - day_name: The name of the day to filter trips by.

    Returns:
    - A DataFrame with trips that run on the specified day, sorted by arrival time.
    """
    # trip_df = pd.merge(trip_df, calendar_df, on='service_id')
    # trip_df = trip_df[trip_df[day_name] == 1]
    # trip_df = trip_df.sort_values(by='arrival_time').reset_index(drop=True)
    # return trip_df
    trip_at_SFU_service = pd.merge(trip_df, calendar_df, on='service_id')
    filtered_trip = trip_at_SFU_service[trip_at_SFU_service[day_name]==1]
    selected_columns = ['trip_id', 'arrival_time', day_name]
    filtered_trip = filtered_trip[selected_columns]
    filtered_trip= filtered_trip.sort_values(by='arrival_time')
    filtered_trip = filtered_trip.reset_index(drop=True)
    return filtered_trip

def convert_time(time_str):
    """Converts time strings into timedelta, adjusting for times beyond 24:00:00."""
    hours, minutes, seconds = map(int, time_str.split(':'))
    if hours >= 24:
        hours -= 24  # Adjust hours to 0-23 range
        return pd.Timedelta(days=1) + pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)
    else:
        return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)

def calculate_time_diff_and_period(df):
    """
    Calculates time differences between consecutive buses and assigns period based on arrival time.

    Parameters:
    - df: DataFrame with trip data, must contain 'arrival_time' column.

    Returns:
    - DataFrame with additional columns for time difference and period.
    """
    df['timedelta'] = df['arrival_time'].apply(convert_time)
    df['time_diff'] = df['timedelta'].diff().dt.total_seconds() / 60
    df['time_diff'].fillna(0, inplace=True)
    df.drop('timedelta', axis=1, inplace=True)
    return df
    # pass
