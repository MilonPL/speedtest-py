import os
import re
import subprocess
import time
from influxdb import InfluxDBClient

# Run speedtest command and capture the output

speedtest_output = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')


# Extract imformation from the speedtest output using regex
ping = re.search('Latency:\s+(.*?)\s', speedtest_output, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', speedtest_output, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', speedtest_output, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', speedtest_output, re.MULTILINE)

# Check if values exist
ping = ping.group(1) if ping else "FAILED"
download = download.group(1) if download else "FAILED"
upload = upload.group(1) if upload else "FAILED"
jitter = jitter.group(1) if jitter else "FAILED"

# Define the path to the CSV file
# Make sure to replace "milon" with your username
csv_file_path = '/home/milon/speedtest/speedtest.csv'

# Try to open the CSV file and write headers if it's emptty
try: 
	with open(csv_file_path, 'a+') as f:
		if os.stat(csv_file_path).st_size == 0:
			f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
except:
	pass

# Write the results to the CSV file
with open(csv_file_path, 'a+') as f:
	f.write('{},{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload))

# Data for InfluxDB
speed_data = [
	{
		"measurement": "internet_speed",
		"tags": {
			"host": "device1"
		},
		"fields": {
			"download": float(download),
			"upload": float(upload),
			"ping": float(ping),
			"jitter": float(jitter)
		}
	}
]

# Connect to InfluxDB
# Port, username, password, database
client = InfluxDBClient('localhost', 8086, 'speedmon', 'password', 'speedtest')
client.write_points(speed_data)
