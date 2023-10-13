#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 2023
CSV format checker

1. check the column number and names (should be the same as SPECs or template files)
2. print unknown columns
3. check how many rows are identical
4. check the data format (time, gps latitude/longtitude, RSSI,...)

@author: Rui

Note: This script is just a simply format checker, 
      the result of this script is only FYI.
"""

import pandas as pd # run the command if error: "pip3 install pandas"

file_path = input("Please give your csv file path: ")
try:
    df = pd.read_csv(file_path, index_col=False)
except Exception as e:
    print("Failed to read the csv file, error: {e}")
    exit(0)
else:
    print("read csv file...")


column_numbers = 16
accepted_col_names=['bssid',
 'channel width (in mhz)',
 'channel width (mhz)',
 'frequency',
 'frequency (ghz)',
 'frequency (in ghz)',
 'gps accuracy',
 'gps accuracy (meters)',
 'gps accuracy (in meters)',
 'gps latitude',
 'gps longitude',
 'network',
 'network channel',
 'network delay (in ms)',
 'network delay (ms)',
 'network interface',
 'noise level (dbm)',
 'noise level (in dbm)',
 'os',
 'public ip address',
 'rssi (dbm)',
 'rssi (in dbm)',
 'ssid',
 'time',
 'wi-fi standard']


# 1. check the column number and names (should be the same as SPECs or template files)
print("column amount check: ...", end="")
if len(df.columns) == column_numbers:
    print("passed")
else:
    print(f"failed, should have {column_numbers} columns")

print("column name check: ...", end="")    
     

# 2. print unknown columns
# your dataset columns in lowercase
df_cols= set([i.lower() for i in df.columns])
diff_cols = df_cols.difference(set(accepted_col_names))
if diff_cols:
    print(f"failed, unknown column names: {diff_cols}")

else:
    print("passed")


# 3. check how many rows are identical
df.columns = df.columns.str.lower()
duplicate_rows = df[df.duplicated()]
num_identical_rows = len(duplicate_rows)
print(f"Number of duplicate rows: {len(duplicate_rows)}")


# 4.Iterate through columns and check the format
# print out all the column types
#for column in df.columns:
#    print(f"Column '{column}' has data type: {df[column].dtype}")

print("Column types check: ...")
expected_formats = {
        'time': int,
        'gps latitude': float,
        'gps longitude': float,
        'network channel': int,
        'channel width (in mhz)': float,
        'channel width (mhz)': float,
        'rssi (dbm)': float,
        'rssi (in dbm)': float,
        'noise level (dbm)': float,
        'noise level (in dbm)': float,
        'network delay (ms)': float,
        'network delay (in ms)': float
    }

for column, expected_type in expected_formats.items():
    try:
        if df[column].dtype != expected_type and df[column].dtype != "int":
            print(f"Error: Column '{column}' has an unexpected data type. Expected {expected_type}, but found {df[column].dtype}.")
            df[column] = df[column].astype(expected_type) # try to fix the data type
    except KeyError:
        pass
    except ValueError:
        print(f"Warning: Unable to convert '{column}' to the expected data type.")
print("Done.")


# output the correct format csv file to a new file
# enable next line if you want the script to save the change on the types of the 
# df.to_csv("./formatted_data.csv", index=False)


