import datetime
import glob
import json
from multiprocessing import Pool

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

num_of_dfs = 16

counter = 0
error_counter = 0

def calculate_shortest_path(x1, y1, x2, y2):
    global counter
    counter += 1
    print(f"Shortest path: {counter}/{counter_size}")
    source = ox.distance.nearest_nodes(G, x1, y1)
    destination = ox.distance.nearest_nodes(G, x2, y2)
    return nx.shortest_path_length(G, source, destination, weight="length")


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
    global counter, error_counter
    counter += 1
    print(f"Avg traffic: {counter}/{counter_size}")
    closest = get_closest_traffic_station(x, y)
    a = relevant_traffic_data.loc[
        (relevant_traffic_data["bin_number"] == bin_number) &
        (relevant_traffic_data["day_number"] == day_number) &
        (relevant_traffic_data["location_id"] == closest)
        ]["avg_speed"]
    try:
        return a.iloc[0]
    except:
        # Return station average, if the specific data fetch failed.
        error_counter += 1
        print(f"Errors: {error_counter}")
        return avg_speeds[closest]


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
#print(avg_speeds)

all_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/../orders_autumn_2020.csv")
all_data = all_data.drop(columns=["ACTUAL_DELIVERY_MINUTES - ESTIMATED_DELIVERY_MINUTES"])

# Add time columns
all_data["BIN_NUMBER"] = all_data["TIMESTAMP"].apply(get_bin_number)
all_data["MONTH"] = all_data["TIMESTAMP"].apply(get_month)
all_data["DAY_NUMBER"] = all_data["TIMESTAMP"].apply(get_day_number)
all_data["WEEK_DAY"] = all_data["TIMESTAMP"].apply(get_week_day)

# Optimize traffic data calculation by taking smaller subset of all data.
relevant_traffic_data = traffic_data.loc[
    (traffic_data["bin_number"].isin(all_data["BIN_NUMBER"])) |
    (traffic_data["day_number"].isin(all_data["DAY_NUMBER"]))
]


#all_data = all_data[0:180]
data_length = len(all_data)
counter_size = 2 * (data_length // num_of_dfs)


dfs = []
for i in range(0, data_length, data_length // num_of_dfs):
    dfs.append(all_data[i:i+data_length // num_of_dfs].copy())


def parallel_calcs(df):
    df["DELIVERY_LENGTH"] = np.vectorize(calculate_shortest_path)(
        df["USER_LAT"],
        df["USER_LONG"],
        df["VENUE_LAT"],
        df["VENUE_LONG"]
    )

    df["AVG_TRAFFIC_SPEED"] = np.vectorize(get_avg_traffic_speed)(
        df["VENUE_LAT"],
        df["VENUE_LONG"],
        df["BIN_NUMBER"],
        df["DAY_NUMBER"]
    )
    return df


counter = 0
workers = []
#with ThreadPoolExecutor(max_workers=num_of_dfs) as executor:
with Pool(num_of_dfs) as p:
    results = p.map(parallel_calcs, dfs)
#    for i in range(0, num_of_dfs):
#        workers.append(
#            executor.submit(parallel_calcs, i, dfs[i])
#        )
#    as_completed(workers)


now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
for i in range(0, num_of_dfs):
    print(f"Writing part {i}")
    try:
        if i == 0:
            with open(f"{DATA_DIR}/combined_data_{now}.csv", "a") as combined_data:
                results[i].to_csv(combined_data)
        else:
            with open(f"{DATA_DIR}/combined_data_{now}.csv", "a") as combined_data:
                results[i].to_csv(combined_data, header=False)
    except:
        print(f"Failed to write part {i}")


"""
Inputs for the model:
OK - Delivery start location lat
OK - Delivery start location lon
OK - Length of the delivery trip

OK - Delivery end location lat
OK - Delivery end location lon
or
Direction of the delivery?

OK - Day of the week
OK - Month of the year
OK - time of the day (5 minute interval)
OK - Delivery estimate
OK - average traffic speed  (average for that 5 minute period from the closest traffic points)
OK - average number of cars (average for that 5 minute period from the closest traffic points)
OK - Item count in the order
OK - CLOUD_COVERAGE
OK - TEMPERATURE
OK - WIND_SPEED
OK - PRECIPITATION
"""
