import pandas as pd

def read_gtfs_files(data_path):
    """
    Reads necessary GTFS static files from the given directory and returns them as DataFrames.

    Parameters:
    - data_path: The file path to the directory containing GTFS static data files.

    Returns:
    - A tuple of DataFrames containing the data from the routes, trips, stops, stop_times, and calendar GTFS files.
    """
    routes_df = pd.read_csv(f'{data_path}/routes.txt')
    trips_df = pd.read_csv(f'{data_path}/trips.txt')
    stops_df = pd.read_csv(f'{data_path}/stops.txt')
    stop_times_df = pd.read_csv(f'{data_path}/stop_times.txt')
    calendar_df = pd.read_csv(f'{data_path}/calendar.txt')

    return routes_df, trips_df, stops_df, stop_times_df, calendar_df
