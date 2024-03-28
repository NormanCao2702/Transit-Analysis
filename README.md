# Transit-Analysis

Question 1:
For Bus 145. How often is Bus 145 late to get to SFU transportation 3 and vice versa?

Steps:

1. Identify Route ID for Bus 145
   • Use routes.txt to find the route ID that corresponds to Bus 145. This file will list all the routes operated by the transit service, and you should look for a row where the route's name or description includes "145" and possibly "Production Way" and "SFU" to confirm it's the correct route.
2. Determine Trip IDs for Both Directions
   • Once you have the route ID, you'll need to find all trip IDs associated with this route in both directions. This information may be in a file like trips.txt, which you mentioned wasn't explicitly listed but is typically part of GTFS data. This file links route IDs to specific trips and includes a direction ID (0 for one direction and 1 for the opposite direction, which could correspond to Production Way to SFU and SFU to Production Way).
3. Analyze Scheduled vs. Actual Times
   • With trip IDs in hand, consult stop_times.txt for the scheduled arrival times at the origin and destination stops for each trip. If your dataset includes actual arrival times (perhaps in a real-time feed or a separate performance dataset), you would compare these actual times against the scheduled times from stop_times.txt to determine lateness.
   • If actual times are not part of your GTFS dataset, you might need to source this data from another place, possibly an API provided by the transit agency that offers real-time bus location and timing data.
4. Calculating Lateness
   • For each trip, calculate the difference between the actual arrival time at the final destination and the scheduled arrival time. Positive values indicate lateness, while negative values indicate early arrival. You can then aggregate this data to see how often Bus 145 is late, the average delay, and any patterns in the timing (e.g., time of day, day of the week).
