# Intro_to_DS_project


## Report
https://docs.google.com/document/d/1wc7nV0eLDa1LZVALbDHhM_T3baqWq5M58YY0rBG-0QQ/edit?usp=sharing

## Data

### digitraffic
https://vayla.fi/vaylista/aineistot/avoindata/tiestotiedot/lam-tiedot

#### Raw data
Tulostiedoston kuvaus
Tulostiedosto on puolipistein eroteltu CSV –tiedosto, jossa on seuraavat kentät. (mittayksikkö suluissa) Kellonaika on Suomen aika, eli EET, tai kesäaikana EEST.
    pistetunnus
    vuosi
    päivän järjestysnumero
    tunti
    minuutti
    sekunti
    sadasosasekunti
    pituus (m)
    kaista
    suunta
    ajoneuvoluokka
    nopeus (km/h)
    faulty (0 = validi havainto, 1=virheellinen havainto)
    kokonaisaika (tekninen)
    aikaväli (tekninen)
    jonoalku (tekninen)

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


Inputs for the model:
Delivery start location lat
Delivery start location lon
Length of the delivery trip

Delivery end location lat
Delivery end location lon
or
Direction of the delivery?

Day of the week
Month of the year
time of the day (5 minute interval)
Delivery estimate
average traffic speed  (average for that 5 minute period from the closest traffic points)
average number of cars (average for that 5 minute period from the closest traffic points)
Item count in the order
CLOUD_COVERAGE
TEMPERATURE
WIND_SPEED
PRECIPITATION


Output for the model:
Actual delivery time



TODO:

DONE - Document the downloaded and processed data
- Impute the missing values to the traffic data.
- Look at the data (Visualizations?)
Started - Make one dataframe that has the delivery dates and traffic data of the same time period joined.
- Create the model that predicts delivery time from the other data

- Update the web app so that you can enter the location of your home and the restaurant
- Show our estimate to the user
  
(- Calculate some statistics on where and when the deliveries are on time or late and show these on map.)


Report TODO:
- Document methods used
- Document data sued and how it was processed
- Check if our results are any better than Wolt estimates
- Conclusions?

- what worked?
- What didn't (and why)?
- What changes did you have to make from your initial plan and why?
- What would you have done differently now? What would possible future steps be?



