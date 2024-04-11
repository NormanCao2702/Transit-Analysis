import pandas as pd

# Cluster Mappings
cluster_mappings = {
    '145': {
        'monday': {0: 'Morning', 1: 'Late Afternoon', 2: 'Night', 3: 'Midday', 4: 'Overnight'},
        'saturday': {0: 'Midday', 1: 'Night', 2: 'Morning', 3: 'Late Afternoon', 4: 'Overnight'},
        'sunday': {0: 'Night', 1: 'Midday', 2: 'Morning', 3: 'Late Afternoon', 4: 'Overnight'}
    },
    '144': {
        'monday': {0: 'Midday', 1: 'Night', 2: 'Morning', 3: 'Late Afternoon', 4: 'Overnight'},
        'saturday': {0: 'Midday', 1: 'Night', 2: 'Morning', 3: 'Late Afternoon', 4: 'Overnight'},
        'sunday': {0: 'Midday', 1: 'Night', 2: 'Morning', 3: 'Overnight', 4: 'Late Afternoon'}
    },
    '143': {
        'monday': {0: 'Late Afternoon', 1: 'Morning', 2: 'Midday'}
    },
    'R5': {
        'monday': {0: 'Morning', 1: 'Night', 2: 'Midday', 3: 'Overnight', 4: 'Late Afternoon'},
        'saturday': {0: 'Midday', 1: 'Morning', 2: 'Night', 3: 'Overnight', 4: 'Late Afternoon'},
        'sunday': {0: 'Midday', 1: 'Night', 2: 'Overnight', 3: 'Late Afternoon', 4: 'Morning'}
    }
}

def apply_cluster_mapping(route, day):
    csv_file = f"csv/bus_{route}_{day}_clustering.csv"
    df = pd.read_csv(csv_file, index_col=0)

    cluster_names = cluster_mappings.get(route, {}).get(day, {})
    if not cluster_names:
        print(f"No mapping found for {route} on {day}.")
        return

    df['period'] = df['cluster'].map(cluster_names)
    df.drop(columns=['cluster'], inplace=True)
    df.to_csv(csv_file)
    print(f"Updated {csv_file}")

def main():
    routes = ['145', '144', '143', 'R5']
    days = ['monday', 'saturday', 'sunday']

    for route in routes:
        # Dynamically get the days available for each route based on cluster_mappings
        days = cluster_mappings[route].keys()  # This will ensure we only loop through defined days for each route

        for day in days:
            apply_cluster_mapping(route, day)

if __name__ == "__main__":
    main()
