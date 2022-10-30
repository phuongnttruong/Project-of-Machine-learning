import glob
import json

import numpy as np
import pandas as pd
from constants import *
import networkx as nx
from pyrosm import OSM, get_data
from time_functions import get_bin_number, get_week_day, get_month, get_day_number
import osmnx as ox
import geopy.distance

osm = OSM(get_data("helsinki_pbf"))
nodes, edges = osm.get_network(nodes=True)
G = osm.to_graph(nodes, edges, graph_type="networkx")


def calculate_shortest_path(x1, y1, x2, y2):
    source = ox.distance.nearest_nodes(G, x1, y1)
    destination = ox.distance.nearest_nodes(G, x2, y2)
    return nx.shortest_path_length(G, source, destination, weight="length")


# Load station data for the stations for which we have traffic data.
with open(f"{DIGITRAFFIC_DATA_DIR}/station_data.json") as f:
    all_stations = json.loads(f.read())
station_data = {x: all_stations[x] for x in LAM_IDS if x in all_stations.keys()}
print(station_data)

# Load all traffic data for 2020
file_list = glob.glob(f"{DIGITRAFFIC_DATA_DIR}/traffic_averages_*.csv")
traffic_data = pd.concat((pd.read_csv(
    f,
    dtype={'bin_number': str, 'avg_speed': float, 'vehicle_count': int, 'day_number': str, 'location_id': str}) for f in file_list),
    ignore_index=True
)
print(traffic_data)
avg_speeds = traffic_data.groupby("location_id").median().get("avg_speed").to_dict()
print(avg_speeds)

all_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/../orders_autumn_2020.csv")
all_data = all_data.drop(columns=["ACTUAL_DELIVERY_MINUTES - ESTIMATED_DELIVERY_MINUTES"])

# TODO: This fails to NodeNotFound error
# all_data["DELIVERY_LENGTH"] = calculate_shortest_path(
#     all_data["USER_LAT"],
#     all_data["USER_LONG"],
#     all_data["VENUE_LAT"],
#     all_data["VENUE_LONG"]
# )

# Add time columns
all_data["BIN_NUMBER"] = all_data["TIMESTAMP"].apply(get_bin_number)
all_data["MONTH"] = all_data["TIMESTAMP"].apply(get_month)
all_data["DAY_NUMBER"] = all_data["TIMESTAMP"].apply(get_day_number)
all_data["WEEK_DAY"] = all_data["TIMESTAMP"].apply(get_week_day)


#all_data = all_data[0:100]


def get_closest_traffic_station(x, y):
    closest = '11'
    shortest = 9999999.0
    for k, v in station_data.items():
        dist = geopy.distance.geodesic((y, x), (v['coordinates'][0], v['coordinates'][1]))
        if dist < shortest:
            closest = k,
            shortest = dist
    return closest[0]


def get_avg_traffic_speed(x, y, bin_number, day_number):
    # TODO: Search three closest measurement points and calculate average.
    #  Now just hard-coded to return station 101 values.
    closest = get_closest_traffic_station(x, y)
    a = traffic_data.loc[
        (traffic_data["bin_number"] == bin_number) &
        (traffic_data["day_number"] == day_number) &
        (traffic_data["location_id"] == closest)
    ]["avg_speed"]
    return a


all_data["avg_traffic_speed"] = np.vectorize(get_avg_traffic_speed)(
    all_data["VENUE_LAT"],
    all_data["VENUE_LONG"],
    all_data["BIN_NUMBER"],
    all_data["DAY_NUMBER"]
)

print(all_data)

"""
Inputs for the model:
OK - Delivery start location lat
OK - Delivery start location lon
Length of the delivery trip

OK - Delivery end location lat
OK - Delivery end location lon
or
Direction of the delivery?

OK - Day of the week
OK - Month of the year
OK - time of the day (5 minute interval)
OK - Delivery estimate
average traffic speed  (average for that 5 minute period from the closest traffic points)
average number of cars (average for that 5 minute period from the closest traffic points)
OK - Item count in the order
OK - CLOUD_COVERAGE
OK - TEMPERATURE
OK - WIND_SPEED
OK - PRECIPITATION
"""
