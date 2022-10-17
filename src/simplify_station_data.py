import json
from constants import *

station_data = dict()

with open(f"{DIGITRAFFIC_DATA_DIR}/lam_stations.json") as f:
    raw_station_data = json.loads(f.read())

for station in raw_station_data["features"]:
    station_data[station["properties"]["tmsNumber"]] = {
        "coordinates": station["geometry"]["coordinates"],
        "name": station["properties"]["name"],
        "municipality": station["properties"]["municipality"]
    }

with open(f"{DIGITRAFFIC_DATA_DIR}/station_data.json", "w") as f:
    f.write(json.dumps(station_data))
