import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

def analyze_bus_data(route):
    """
    Analyzes bus data for a given route, performing statistical tests and generating a histogram.

    Parameters:
    - route: The bus route number as a string.
    """
    days = ['sunday', 'monday', 'saturday']
    data_frames = []

    for day in days:
        # Load the data
        df = pd.read_csv(f"csv/bus_{route}_{day}_clustering.csv")
        df['day_type'] = day.capitalize()
        data_frames.append(df)

    # Combine the datasets
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Perform and display statistical tests
    perform_statistical_tests(combined_data)

    # Plot a histogram of the time differences
    plot_time_diff_histogram(combined_data, route)

def perform_statistical_tests(data):
    """
    Performs statistical tests on the combined data.
    """
    print('Normality test statistics:', *stats.normaltest(data['time_diff']))
    print('Levene’s test statistics:', *stats.levene(
        data[data['day_type'] == 'Sunday']['time_diff'],
        data[data['day_type'] == 'Monday']['time_diff'],
        data[data['day_type'] == 'Saturday']['time_diff']
    ))

    for day1 in ['Sunday', 'Monday']:
        for day2 in ['Saturday', 'Monday', 'Sunday']:
            if day1 != day2:
                u_statistic, p_value = mannwhitneyu(
                    data[data['day_type'] == day1]['time_diff'],
                    data[data['day_type'] == day2]['time_diff'],
                    alternative='two-sided'
                )
                print(f'Mann-Whitney U test statistic comparing {day1} and {day2}:', u_statistic, 'p-value:', p_value)

def plot_time_diff_histogram(data, route):
    """
    Plots a histogram of time differences for the combined data.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(data['time_diff'], bins=30, kde=True)

    plt.title(f'Histogram of Time Differences for Bus {route} across Days')
    plt.xlabel('Time Difference (minutes)')
    plt.ylabel('Frequency')
    plt.savefig(f'bus-histogram/{route} histogram.png')
    # plt.show()

def main():
    # Analyze data for each bus route
    for route in ['144', '145', 'R5']:
        analyze_bus_data(route)

# if __name__ == "__main__":
#     main()
