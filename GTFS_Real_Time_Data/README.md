# GTFS - Real Time Data
## Steps
1. Get the real-time data from Translink
2. Extract the real-time data
3. Clean the data and generate the output column
4. Analyze the outputs
5. Train and evaluate the model

<br>

## Step 1: Get the real-time data from Translink
**Program: record_real_time_data.py**
- This program gets the real-time data from Translink every minute.
- The real-time data is stored in the **real_time_data** directory as JSON format.
- Since the maximum number of API requests per day is 1000, I only recorded the data from 7 am to 23 pm with the bus routes 144, 145, and R5.

Remarks:
- The testing API key is only for testing. Please use your API key for long testing.

<br>

**File: real_time_data/*.json**
- The filename format is RouteNumber_YearMonthDay_HourMinuteSecond.

<br>

## Step 2: Extract the real-time data
**Program: extract_real_time_data.py**
- This program generates a JSON file from all the real-time data named **extracted_real_time_data.json**.
- This extracted data will exclude invalid data, for example, server error messages and no buses in this route message.
- This program will also generate an extraction report named **extraction_report.json**.

<br>

**File: data/extracted_real_time_data.json**
- A JSON file that combines all the real-time data.

<br>

**File: data/extraction_report.json**
- A JSON file that records the data count, file count, valid file count, invalid file count, names of invalid files..

<br>

## Step 3: Clean the data and generate the OnTime column
**Program: clean_data.ipynb**
- This progam cleans the real time data and the static data and generates the OnTime column with the following steps.
- The output is a JSON file named **cleaned_data.json**.

<br>

Real Time Data (Cleaning)
| Step | Description |
| :- | :- |
| 1 | Convert the time strings to datetime.time objects |
| 2 | Convert the time strings to datetime.date objects |
| 3 | Drop the unrelated columns |
| 4 | Drop all null values |
| 5 | Drop all duplicates |
| 6 | Filter the recorded hour bewteen 7:00 to 23:00 |
| 7 | Filter the recorded date bewteen April 7 to April 10 |
| 8 | Remove all outliers of Latitude and Longitude |

<br>

Static Data (Cleaning)
| Step | Description |
| :- | :- |
| 1 | Drop the unrelated columns (stop_times.txt) |
| 2 | Filter the trip_id which is in the real time data |
| 3 | Convert the time strings to the datatime.time objects |
| 4 | Drop the unrelated columns (stops.txt) |
| 5 | Merge the stop times data and the stops data |
| 6 | Drop the unrelated columns (merged data frame) |

Remarks:
- static_data/stop_times.txt is removed due to the size limit. Please download the file from the link https://gtfs-static.translink.ca/gtfs/History/2024-04-05/google_transit.zip.

<br>

OnTime Column (Generating)
- Calculate the distance between the closest bus stop and the bus. If the distance is larger than 10m, then this real time data is deleted.
- Calculate the time difference between the arrival time of the closest bus stop and the GPS recorded time. If the time difference smaller than the threshold, then the bus is labeled as OnTime.

<br>

**File: cleaned_data.json**
- A JSON file that contains the cleaned data.

<br>

## Step 4: Analyze the OnTime column.
**Program: analyze_data.ipynb**
- Analyze the output column.

<br>

## Step 5: Train and evaluate the model
**Program: train_model.ipynb**
- Train the RandomForestClassifier to predict the outputs.

<br>
