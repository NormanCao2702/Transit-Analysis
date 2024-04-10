# GTFS - Real Time Data
## Steps
1. Get the real-time data from Translink
2. Extract the real-time data
3. Clean the data and extract the features
4. Apply the data to machine learning models
5. Evaluate the machine learning models

<br>

## Step 1: Get the real-time data from Translink
**Program: record_real_time_data.py**
- This program gets the real-time data from Translink every minute.
- The real-time data is stored in the **real_time_data** directory as JSON format.
- Since the maximum number of API requests per day is 1000, I only recorded the data from 7 am to 23 pm with the bus routes 144, 145, and R5.

Remarks:
- The testing API key is only for testing. Please use your API key for long testing.

**File: real_time_data/*.json**
- The filename format is RouteNumber_YearMonthDay_HourMinuteSecond.

<br>

## Step 2: Extract the real-time data
**Program: extract_real_time_data.py**
- This program generates a JSON file from all the real-time data named **extracted_real_time_data.json**.
- This extracted data will exclude invalid data, for example, server error messages and no buses in this route message.
- This program will also generate an extraction report named **extraction_report.json**.

**File: extracted_real_time_data.json**
- A JSON file that combines all the real-time data.

**File: extraction_report.json**
- A JSON file that records the data count, file count, valid file count, invalid file count, names of invalid files..

<br>

## Step 3: Clean the data and extract the features
**Program: clean_real_time_data.ipynb**
- This progam cleans the real time data with the following steps.
1. Convert the date and time strings to datetime
2. Drop the unused columns
3. Drop all null values
4. Drop all duplicates
5. Filter the recorded hour bewteen 7:00 to 23:00
6. Remove all outliers

<br>

## Step 4: Apply the data to machine learning models
- On scheduled

<br>

## Step 5: Evaluate the machine learning models
- On scheduled

<br>
