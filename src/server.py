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

# Get list of unique station IDs
station_ids = [str(int(x)) for x in traffic_data["location_id"].dropna().unique().tolist()]
#print(station_ids)

# Load station data for the stations for which we have traffic data.
with open(f"{DIGITRAFFIC_DATA_DIR}/station_data.json") as f:
    all_stations = json.loads(f.read())
station_data = {x: all_stations[x] for x in station_ids if x in all_stations.keys()}
#print(station_data)

base_color = "#FF0000"

urls = (
    '/map', 'index'
)

web.config.debug = True


def get_latest_traffic():
    now = datetime.now(pytz.timezone("Europe/Helsinki"))
    day_number = now.timetuple().tm_yday
    bin_number = now.hour * 12 + (now.minute // 5) * 5
    return traffic_data.loc[
        (traffic_data['day_number'] == day_number) &
        (traffic_data['bin'] == bin_number) &
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


def update_map(data_points):
    avg_lat, avg_long, zoom = get_initial_params()
    entry_map = folium.Map(
        location=[avg_lat, avg_long],
        zoom_start=zoom
    )
    for point in data_points.to_dict(orient="records"):
        this_station = station_data[str(int(point["location_id"]))]
        print(this_station)
        folium.CircleMarker(
            location=(this_station["coordinates"][1], this_station["coordinates"][0]),
            radius=30,
            color=base_color,
            fill=True,
            # fill_color=base_color,
        ).add_to(entry_map)
    return entry_map._repr_html_()
    # entry_map.save(html_str)


class index:
    def GET(self):
        traffic_now = get_latest_traffic()
        return update_map(traffic_now)
        # with open("map.html", "r") as f:
        #     return f.read()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
