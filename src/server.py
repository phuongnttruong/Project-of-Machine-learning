#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import requests

import folium
import json

import statistics
import web
import pandas as pd
from constants import *

HELSINKI_TZ = "Europe/Helsinki"

REAL_TIME_TRAFFIC_URL = "https://tie.digitraffic.fi/api/v1/data/tms-data"

# Load all traffic data for 2020
file_list = glob.glob(f"{DIGITRAFFIC_DATA_DIR}/traffic_averages_*.csv")
traffic_data = pd.concat((pd.read_csv(f) for f in file_list), ignore_index=True)
avg_speeds = traffic_data.groupby("location_id").median().get("avg_speed").to_dict()
avg_speeds = {str(int(x)): avg_speeds[x] for x in avg_speeds}
# print(avg_speeds)

# Get list of unique station IDs
station_ids = [str(int(x)) for x in traffic_data["location_id"].dropna().unique().tolist()]
#print(station_ids)

# Load station data for the stations for which we have traffic data.
with open(f"{DIGITRAFFIC_DATA_DIR}/station_data.json") as f:
    all_stations = json.loads(f.read())
station_data = {x: all_stations[x] for x in station_ids if x in all_stations.keys()}
#print(station_data)

base_color = 1.0

urls = (
    '/', 'index'
)

web.config.debug = True


def get_latest_traffic():
    current_traffic = {}
    r = requests.get(REAL_TIME_TRAFFIC_URL, headers=HEADERS)
    for item in r.json()["tmsStations"]:
        station_id = str(item["tmsNumber"])
        if station_id in station_ids:
            current_traffic[station_id] = item
    return current_traffic


def get_initial_params():
    latitudes = []
    longitudes = []
    for station in station_data:
        longitudes.append(station_data[station]["coordinates"][0])
        latitudes.append(station_data[station]["coordinates"][1])
    zoom = 12
    return statistics.mean(latitudes), statistics.mean(longitudes), zoom


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def get_marker_color(avg_speed, location_id):
    avg_speed_for_station = avg_speeds[location_id]
    if avg_speed < 0.8 * avg_speed_for_station:
        color = (255, 0, 0)
    elif avg_speed < 0.95 * avg_speed_for_station:
        color = (255, 255, 0)
    else:
        color = (0, 255, 0)
    return rgb_to_hex(color)


def update_map(data_points):
    avg_lat, avg_long, zoom = get_initial_params()
    entry_map = folium.Map(
        location=[avg_lat, avg_long],
        zoom_start=zoom
    )

    for id, values in data_points.items():
        this_station = station_data[id]
        avg_speed_now = calculate_avg_speed(values)
        if not avg_speed_now:
            continue
        marker_color = get_marker_color(avg_speed_now, id)
        folium.CircleMarker(
            location=(this_station["coordinates"][1], this_station["coordinates"][0]),
            radius=30,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            tooltip=
            f"""
            <table>
            <tr><td>Average speed now:</td><td>{round(avg_speed_now, 2)} km/h</td></tr>
            <tr><td>Average speed overall:</td><td>{round(avg_speeds[id], 2)} km/h</td></tr>
            </table>
            """
        ).add_to(entry_map)
    return entry_map._repr_html_()


def calculate_avg_speed(values):
    pass1 = 0
    pass2 = 0
    avg1 = 0
    avg2 = 0
    for sensorValue in values['sensorValues']:
        if sensorValue['id'] == 5116:
            pass1 = sensorValue['sensorValue']
        elif sensorValue['id'] == 5119:
            pass2 = sensorValue['sensorValue']
        elif sensorValue['id'] == 5122:
            avg1 = sensorValue['sensorValue']
        elif sensorValue['id'] == 5125:
            avg2 = sensorValue['sensorValue']
    if (pass1 + pass2) > 0:
        return (pass1 * avg1 + pass2 * avg2) / (pass1 + pass2)
    else:
        return None


def get_html_template():
    with open("templates/map.html") as f:
        return f.read()


class index:
    def GET(self):
        traffic_now = get_latest_traffic()
        html_template = get_html_template()
        html = html_template.replace("%map_element%", update_map(traffic_now))
        # html = html_template.replace("%delivery_estimate%", "")
        return html


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
