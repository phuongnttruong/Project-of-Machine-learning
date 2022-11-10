# Final project for machine learning

When placing an order on a delivery application like Wolt or Foodora, it is quite easy to understand that customers want their food to reach their home as soon as possible. With the help of Google Maps or Open Street Map, the delivery companies can estimate the delivery time based on coordinates between customer and the revenue, however, the actual delivery time is affected by many factors besides the distance between two points, and it is not straightforward to estimate. We aim to predict the actual delivery time based on the estimated time given by Wolt and evaluate if the delivery time is affected by the date of orders. 

## Data

### digitraffic

https://vayla.fi/vaylista/aineistot/avoindata/tiestotiedot/lam-tiedot

#### Raw data


#### Average data (traffic_averages_xx.csv)

These files contain traffic data averages for 5 minute intervals for each station in year 2020.

field descriptions:
- bin: 5 minute interval during the day. 0 = 0:00:00-0:04:59, 1 = 0:05:00-0:09:59, 2=0:10:00-0:14.59, etc.
- location_id: ID of the station. This corresponds to the field `features.properties.tmsNumber` in the lam_stations.json.
- day_number: Number of the day during the year. 1 = 1st of January, 2 = 2nd of January, etc.
- avg_speed: Average speed of the vehicles during the 5-minute period. Unit: km/h.
- vehicle_count: Number of vehicles that passed the measurement point during the 5 minute period.


## src

- fetch_digitraffic_data.py: File for fetching traffic data (19GB for year 2021)









