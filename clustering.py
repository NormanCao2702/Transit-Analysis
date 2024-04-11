import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

def convert_time_cluster(time_str):
    """
    Converts a time string into minutes past midnight, adjusting for times beyond 24:00:00.

    Parameters:
    - time_str: A string representing time in HH:MM:SS format.

    Returns:
    - The number of minutes past midnight.
    """
    hours, minutes, seconds = map(int, time_str.split(':'))
    if hours >= 24:
        hours -= 24  # Adjust for times beyond 24:00:00
    total_minutes = hours * 60 + minutes + seconds / 60
    return total_minutes

def apply_clustering(df, n_clusters, random_state, bus_and_day):
    """
    Applies KMeans clustering to the DataFrame based on arrival times and time differences.

    Parameters:
    - df: DataFrame containing the trips data, must include 'arrival_time' and 'time_diff'.
    - n_clusters: The number of clusters to form.
    - random_state: A seed used by the random number generator for reproducibility.
    - bus_and_day: A string identifier for saving output files related to specific bus and day.

    Effects:
    - Saves a CSV file with clustering results.
    - Saves a scatter plot visualizing the clusters.
    """
    df['minutes_past_midnight'] = df['arrival_time'].apply(convert_time_cluster)
    X = df[['minutes_past_midnight', 'time_diff']]

    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=random_state)
    df['cluster'] = kmeans.fit_predict(X)
    columns_needed = ['trip_id','arrival_time','time_diff','minutes_past_midnight','cluster']
    df = df[columns_needed]
    # Save the clustering results to a CSV file
    df.to_csv(f'csv/{bus_and_day}_clustering.csv', index=False)

    # Visualization
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='minutes_past_midnight', y='time_diff', hue='cluster', palette='viridis', alpha=0.7, s=100)
    plt.title(f'{bus_and_day} Cluster Distribution by Minutes Past Midnight and Time Difference')
    plt.xlabel('Minutes Past Midnight')
    plt.ylabel('Time Difference (minutes)')
    plt.legend(title='Cluster')
    plt.savefig(f'schedule-cluster/{bus_and_day}_ScheduleCluster.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the plot to free up memory
