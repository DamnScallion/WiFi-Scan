import subprocess
import re
import time
import pandas as pd

def getIP():
    try:
        response = subprocess.check_output(["ping", "-c", "1", "cse.unsw.edu.au"]).decode()
        ip = re.search(r"\(([\d.]+)\)", response).group(1)
        return ip
    except:
        return None

def getDelay():
    try:
        response = subprocess.check_output(["ping", "-c", "1", "cse.unsw.edu.au"]).decode()
        if "Request timeout" in response:
            return 4000.0
        delay = float(re.search(r"time=([\d.]+)", response).group(1))
        return round(delay, 3)
    except:
        return None

def getAccessPoints(airport):
    wifi_list = subprocess.check_output(['sudo', airport, '-s']).decode().splitlines()[1:]
    aps = []

    for wifi in wifi_list:
        info_line = re.split('\s+', wifi, maxsplit=5)
        if '' in info_line:
            info_line.remove('')
        SSID, BSSID, RSSI, channel = info_line[:4]
        if '-' not in RSSI:
            continue
        channel_list = channel.split(',')
        channel = channel_list[0]
        if not channel.isdigit():
            continue
        else:
            frequency = "2.4" if int(channel) <= 14 else "5"
        
        channel_width = "20"
        if len(channel_list) > 1 or frequency == "5":
            channel_width = "40"
        if len(channel_list) > 1 and frequency == "5":
            channel_width = "80"
        aps.append([SSID, BSSID, frequency, channel, RSSI, channel_width])

    return aps

if __name__ == '__main__':
    AIRPORT = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
    connected_wifi = subprocess.check_output([AIRPORT, '-I'])
    SSID = re.search(r'SSID: ([\w-]+)', connected_wifi.decode()).group(1)
    timestamp = int(time.time())

    wifi_standard = "802.11ac"

    public_ip = None
    network_delay = None

    if SSID == 'uniwide':
        public_ip = getIP()
        network_delay = getDelay()
    
    latitude = -33.91905
    longitude = 151.22802
    accuracy = 4.75

    aps = getAccessPoints(AIRPORT)

    data = {
        'time': [],
        'os': [],
        'network interface': [],
        'gps latitude': [],
        'gps longitude': [],
        'gps accuracy (meters)': [],
        'ssid': [],
        'bssid': [],
        'wi-fi standard': [],
        'frequency': [],
        'network channel': [],
        'channel width (in mhz)': [],
        'rssi (in dbm)': [],
        'noise level (in dbm)': [],
        'public ip address': [],
        'network delay (in ms)': []
    }

    for ap in aps:
        data['time'].append(timestamp)
        data['os'].append("MACOS")
        data['network interface'].append("AirPort")
        data['gps latitude'].append(round(latitude, 6))
        data['gps longitude'].append(round(longitude, 6))
        data['gps accuracy (meters)'].append(round(accuracy, 1))
        data['ssid'].append(ap[0])
        data['bssid'].append(ap[1])
        data['wi-fi standard'].append(wifi_standard)
        data['frequency'].append(ap[2])
        data['network channel'].append(int(ap[3]))
        data['channel width (in mhz)'].append(float(ap[5]))
        data['rssi (in dbm)'].append(float(ap[4]))
        data['noise level (in dbm)'].append(float(ap[4]))
        data['public ip address'].append(public_ip if ap[0] == "uniwide" else None)
        data['network delay (in ms)'].append(network_delay if ap[0] == "uniwide" else None)

    df = pd.DataFrame(data)
    print(df)

    # Check if the file exists
    file_exists = False
    try:
        with open('data.csv', 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    # If the file exists, read it and concatenate the new data
    if file_exists:
        existing_data = pd.read_csv('data.csv')
        combined_data = pd.concat([existing_data, df], ignore_index=True)
        combined_data.to_csv('data.csv', index=False)
    else:
        df.to_csv('data.csv', index=False)

    print("Table updated in csv file: data.csv")
    
