#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
from datetime import datetime

import folium
import json

import numpy as np
import pytz
import statistics
import web
import pandas as pd
from constants import *

HELSINKI_TZ = "Europe/Helsinki"

# Load all traffic data for 2021
file_list = glob.glob(f"{DIGITRAFFIC_DATA_DIR}/traffic_averages_*.csv")
traffic_data = pd.concat((pd.read_csv(f) for f in file_list), ignore_index=True)
avg_speeds = traffic_data.groupby("location_id").median().get("avg_speed").to_dict()
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


def get_day_number(now):
    return  now.timetuple().tm_yday


def get_bin_number(now):
    return now.hour * 12 + (now.minute // 5) * 5


def get_latest_traffic():
    now = datetime.now(pytz.timezone("Europe/Helsinki"))
    return traffic_data.loc[
        (traffic_data['day_number'] == get_day_number(now)) &
        (traffic_data['bin'] == get_bin_number(now)) &
        (traffic_data['location_id'] != np.NaN)
    ]


def get_initial_params():
    latitudes = []
    longitudes = []
    for station in station_data:
        print(station)
        longitudes.append(station_data[station]["coordinates"][0])
        latitudes.append(station_data[station]["coordinates"][1])
    zoom = 12
    return statistics.mean(latitudes), statistics.mean(longitudes), zoom


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def get_marker_color(point):
    speed = point['avg_speed']
    avg_speed_for_station = avg_speeds[point['location_id']]
    print(speed, avg_speed_for_station)
    if speed < 0.8 * avg_speed_for_station:
        color = (255, 0, 0)
    elif speed < 0.98 * avg_speed_for_station:
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

    for point in data_points.to_dict(orient="records"):
        this_station = station_data[str(int(point["location_id"]))]
        marker_color = get_marker_color(point)
        print(this_station)
        folium.CircleMarker(
            location=(this_station["coordinates"][1], this_station["coordinates"][0]),
            radius=30,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
        ).add_to(entry_map)
    return entry_map._repr_html_()


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
