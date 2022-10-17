# Intro_to_DS_project


## Report
https://docs.google.com/document/d/1wc7nV0eLDa1LZVALbDHhM_T3baqWq5M58YY0rBG-0QQ/edit?usp=sharing

## Data

### digitraffic
https://vayla.fi/vaylista/aineistot/avoindata/tiestotiedot/lam-tiedot

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

## src

- fetch_digitraffic_data.py: File for fetching traffic data (19GB for year 2021)


Inputs for the model:
Delivery start location (lat, lon)
Delivery end location(lat, lon)
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

Edu - Document the downloaded and processed data
- Impute the missing values to the traffic data.
- Look at the data (Visualizations?)
- Make one dataframe that has the delivery dates and traffic data of the same time period joined.
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



