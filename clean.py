import re
import pandas as pd

# Step 1: Parse the raw text to get the details
with open("wifi_1/wifi_scan copy 1.txt", 'r') as file:
    raw_txt = file.read()

parsed_data = {}

# Extracting details using regex
for match in re.finditer(r'bssid=(?P<bssid>[0-9a-f:]+).*?channel=\[.*?, width=(?P<width>\d+)].*?type=(?P<type>\w+)', raw_txt):
    bssid = match.group("bssid")
    width = match.group("width")
    # type_ = match.group("type")
    type_ = "802." + match.group("type")
    parsed_data[bssid] = {"channel width (in mhz)": width, "wi-fi standard": type_}

# Step 2: Load your data.csv file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Step 3: Update the DataFrame rows based on the BSSID
for bssid, data in parsed_data.items():
    df.loc[df['bssid'] == bssid, 'channel width (in mhz)'] = data['channel width (in mhz)']
    df.loc[df['bssid'] == bssid, 'wi-fi standard'] = data['wi-fi standard']

# Save the changes back to data.csv
df.to_csv('data.csv', index=False)

print("Updated!!!")
