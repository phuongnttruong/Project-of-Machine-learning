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
