# Script for fetching traffic data from Helsinki area from open API
# https://vayla.fi/vaylista/aineistot/avoindata/tiestotiedot/lam-tiedot

import requests

LAM_RAW_DATA_URL = "https://aineistot.vayla.fi/lam/rawdata/20{year}/{ely}/lamraw_{lam_id}_{year}_{day_number}.csv"

# Digitraffic measurement points located in Helsinki
LAM_IDS = [
    "11","101",
    "109","117","119","126","131","145","146","147","148","149","151",
    "152","153","154","155","164","165","172","195","196","197",
]
YEARS = ["21"]

headers = {"Digitraffic-User": "ds-project-app"}

print(f"Fetching {len(LAM_IDS)} measurement points' data")

for lam_id in LAM_IDS:
    for year in YEARS:
        for day in range(1, 366):
            print(f"Fetching {lam_id}, {year}, {day}")
            r = requests.get(
                LAM_RAW_DATA_URL.format(
                    ely="01",  # ID for Uusimaa
                    year=year,
                    lam_id=lam_id,
                    day_number=str(day)
                ),
                headers=headers
            )
            with open(f"../data/digitraffic/raw_traffic_data_{lam_id}_{year}_{day}.csv", "w") as f:
                f.write(r.text)
