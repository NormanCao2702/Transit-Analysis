import pandas as pd
# from data_loading import read_gtfs_files
# from data_processing import (filter_by_route, filter_by_stop, filter_trips_by_route_and_direction,
#                              filter_stop_times_by_trip_and_stop, get_trips_by_day, calculate_time_diff_and_period)
# from clustering import apply_clustering
# from cluster_mapping import map_clusters_to_periods, calculate_average_time_diff
from statistic import analyze_bus_data
from heatmap import load_and_process_csv, plot_heatmap

def main():
    # plotting heatmap
    day_order = ['Weekday', 'Saturday', 'Sunday']
    routes_days = {
            '145': ['monday', 'saturday', 'sunday'],
            '144': ['monday', 'saturday', 'sunday'],
            '143': ['monday'],  # Bus 143 only runs on weekdays
            'R5': ['monday', 'saturday', 'sunday']
        }

    for route, days in routes_days.items():
            print(f"Processing Bus {route}...")
            df_all_days = load_and_process_csv(route, days)
            plot_heatmap(df_all_days,route)

    # Analyze data for each bus route
    for route in ['144', '145', 'R5']:
        analyze_bus_data(route)

if __name__ == "__main__":
    # Call your main function or the primary entry point function here
    main()
