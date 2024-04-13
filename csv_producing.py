from data_loading import read_gtfs_files
from data_processing import (filter_by_route, filter_by_stop, filter_trips_by_route_and_direction,
                             filter_stop_times_by_trip_and_stop, get_trips_by_day, calculate_time_diff_and_period)
from clustering import apply_clustering
import pandas as pd

# Configuration
DATA_PATH = 'GTFS-Static-Data'
ROUTES_INFO = {
    '145': {'n_clusters': 5, 'days': ['monday', 'saturday', 'sunday']},
    '144': {'n_clusters': 5, 'days': ['monday', 'saturday', 'sunday']},
    'R5': {'n_clusters': 5, 'days': ['monday', 'saturday', 'sunday']},
    '143': {'n_clusters': 3, 'days': ['monday']}  # 143 operates only on Monday
}
RANDOM_STATE = 42

def process_route_day_combinations(data_path, routes_info, random_state):
    """
    Processes each route and day combination through the workflow of data loading, processing, and clustering.

    Parameters:
    - data_path: The path to the directory containing the GTFS data files.
    - routes_info: A dictionary with route short names as keys, their corresponding n_clusters,
      and the days they operate as values.
    - random_state: Seed for the random number generator used in clustering for reproducibility.
    """
    # Load GTFS data
    routes_df, trips_df, stops_df, stop_times_df, calendar_df = read_gtfs_files(data_path)

    for route_short_name, info in routes_info.items():
        route_id = filter_by_route(routes_df, route_short_name)
        stop_id = filter_by_stop(stops_df, 'SFU Transportation Centre @ Bay 2')
        trips_by_day = None
        trips_df_filtered = None
        stop_times_filtered = None
        for day in info['days']:
            trips_df_filtered = filter_trips_by_route_and_direction(trips_df, route_id, 0)
            stop_times_filtered = filter_stop_times_by_trip_and_stop(stop_times_df, trips_df_filtered, stop_id)
            trips_by_day = get_trips_by_day(stop_times_filtered, calendar_df, day)
            trips_by_day = calculate_time_diff_and_period(trips_by_day)

            # Apply clustering
            bus_and_day = f'bus_{route_short_name}_{day}'
            apply_clustering(trips_by_day, info['n_clusters'], random_state, bus_and_day)

if __name__ == "__main__":
    process_route_day_combinations(DATA_PATH, ROUTES_INFO, RANDOM_STATE)
