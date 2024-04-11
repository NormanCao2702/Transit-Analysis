import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process_csv(route, days):
    """Load CSV files for given route and days, returning a DataFrame with average time differences."""
    all_days_data = []
    period_order = ['Morning', 'Midday', 'Late Afternoon', 'Night', 'Overnight']

    for day in days:
        csv_file = f'csv/bus_{route}_{day}_clustering.csv'
        df = pd.read_csv(csv_file, index_col=0)
        non_zero_time_diff = df[df['time_diff'] != 0]
        period_avg = non_zero_time_diff.groupby('period')['time_diff'].mean().reset_index()
        # Adjust day naming here
        if day == 'monday':
            period_avg['day'] = 'Weekday'
        else:
            period_avg['day'] = day.capitalize()
        all_days_data.append(period_avg)

    df_all_days = pd.concat(all_days_data)
    df_all_days['period'] = pd.Categorical(df_all_days['period'], categories=period_order, ordered=True)
    return df_all_days


def plot_heatmap(df_all_days, route):
    """Plot a heatmap for the given DataFrame."""
    # Dynamically determine day_order based on the 'day' column in df_all_days
    available_days = df_all_days['day'].unique()

    preferred_order = ['Weekday', 'Saturday', 'Sunday']
    # Use available days but maintain the preferred order
    day_order = [day for day in preferred_order if day in available_days]

    # Pivot the DataFrame and reorder columns based on day_order
    df_pivot = df_all_days.pivot(index='period', columns='day', values='time_diff').reindex(columns=day_order)

    plt.figure(figsize=(10, 7))
    ax = sns.heatmap(df_pivot, annot=True, fmt=".2f", linewidths=.5, cmap='coolwarm')
    ax.set_aspect("equal")
    plt.yticks(rotation=0)
    plt.title(f'Average Time Difference Heatmap by Period and Day for Bus {route}')
    plt.savefig(f'heatmap-pic/Bus{route}Heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the plot to free up memory

def main():
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

if __name__ == "__main__":
    main()
