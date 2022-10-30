# Script for running through raw digitraffic data and parsing speed and vehicle count averages

import pandas as pd
import numpy as np
from constants import *

for lam_id in LAM_IDS:
    for year in YEARS:
        with open(f"{DIGITRAFFIC_DATA_DIR}/traffic_averages_{lam_id}.csv", "w") as year_file:
            for day in range(1, 366):
                print(f"Processing: raw_traffic_data_{lam_id}_{year}_{day}.csv")
                try:
                    df = pd.read_csv(
                        f"{DIGITRAFFIC_DATA_DIR}/raw_traffic_data_{lam_id}_{year}_{day}.csv",
                        delimiter=";",
                        dtype=float,
                        names=COLUMN_NAMES
                    )
                except (FileNotFoundError, pd.errors.EmptyDataError, ValueError):
                    print(f"Missing file raw_traffic_data_{lam_id}_{year}_{day}.csv")
                    df = pd.DataFrame(columns=COLUMN_NAMES)

                # Drop faulty measurements
                df = df.where(df.faulty == 0)

                # Divide the measurements to bins of size BIN_SIZE_MINUTES
                df["bin_n"] = np.floor((df["hour"] * 60 + df["minute"]) / BIN_SIZE_MINUTES)

                df = df.drop(
                    columns=[
                        "year", "hour", "minute", "second", "sub_second", "length", "lane", "direction",
                        "vehicle_type", "faulty", "total_time", "time_diff", "queue_start"
                    ]
                )

                grouped = df.groupby(["bin_n"])

                aggregates = grouped.agg(
                    loc_id=pd.NamedAgg(column="location_id", aggfunc="first"),
                    day_n=pd.NamedAgg(column="day_number", aggfunc="first"),
                    avg_speed=pd.NamedAgg(column="speed", aggfunc="mean"),
                    vehicle_count=pd.NamedAgg(column="bin_n", aggfunc="count")
                )

                # Make sure that each day has all the bins, even if there were no events for that period.
                aggregates = aggregates.reindex(index=np.arange(0, 24*60/BIN_SIZE_MINUTES))

                aggregates = aggregates.dropna()

                # Create string indices
                aggregates.index = aggregates.index.map(int).map(str)
                aggregates.index.names = ['bin_number']
                aggregates["day_number"] = aggregates["day_n"].apply(int).apply(str)
                aggregates["location_id"] = aggregates["loc_id"].apply(int).apply(str)
                aggregates = aggregates.drop(columns=["day_n", "loc_id"])

                if day == 1:
                    aggregates.to_csv(year_file)
                else:
                    aggregates.to_csv(year_file, header=False)
