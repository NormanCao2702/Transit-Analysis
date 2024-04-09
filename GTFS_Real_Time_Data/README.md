# GTFS - Real Time Data
## Steps
1. Get the real-time data from Translink
2. Extract the real-time data
3. Clean the data and extract the features
4. Apply the data to machine learning models
5. Evaluate the machine learning models

<br>

## Step 1: Get the real-time data from Translink
**File: record_real_time_data.py**
- This program gets the real-time data from Translink every minute.
- The real-time data is stored in the **real_time_data** directory as JSON format.
- The filename format is RouteNumber_YearMonthDay_HourMinuteSecond.
- Since the maximum number of API requests per day is 1000, I only recorded the data from 7 am to 23 pm with the bus routes 144, 145, and R5.

Remarks:
- The testing API key is only for testing. Please use your API key for long testing.

**File: record_real_time_data.ipynb**
- This program is the Jupyter version of record_real_time_data.py

<br>

## Step 2: Extract the real-time data
**File: extract_real_time_data.ipynb**
- This program generates a JSON file from all the real-time data named **extracted_real_time_data.json**.
- This extracted data will exclude invalid data, for example, server error messages and no buses in this route message.

<br>

## Step 3: Clean the data and extract the features
- On process

<br>

## Step 4: Apply the data to machine learning models
- On scheduled

<br>

## Step 5: Evaluate the machine learning models
- On scheduled

<br>
