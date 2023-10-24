
# speedtest-py

## Overview

Speedtest-py is a Python tool made for Linux Debian 11. It utilizes the Speedest CLI to measure the connection speed every 5 minutes, then sends it to a .csv file and Grafana.

## Installation

### Install the Speedtest CLI

```bash
apt install apt-transport-https gnupg1 dirmngr lsb-release
curl -L https://packagecloud.io/ookla/speedtest-cli/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/speedtestcli-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/speedtestcli-archive-keyring.gpg] https://packagecloud.io/ookla/speedtest-cli/debian/ $(lsb_release -cs) main" | sudo tee  /etc/apt/sources.list.d/speedtest.list
apt update
apt install speedtest
```

### Install InfluxDB

```bash
curl https://repos.influxdata.com/influxdata-archive.key | gpg --dearmor | sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
apt update
apt install influxdb
apt install python3-influxdb
systecmtl enable influxdb
systemctl start influxdb
```

### Install Grafana
```bash
curl https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana-archive-keyrings.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/grafana-archive-keyrings.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
apt update
apt install grafana
systemctl enable grafana-server
systemctl start grafana-server
```

### Setting up InfluxDB

```bash
influx
CREATE DATABASE speedtest
CREATE USER "speedmon" WITH PASSWORD 'password'
GRANT ALL ON "speedtest" to "speedmon"
```




