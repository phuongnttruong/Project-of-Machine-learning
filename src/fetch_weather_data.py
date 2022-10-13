# see https://www.ilmatieteenlaitos.fi/latauspalvelun-pikaohje
# see https://www.ilmatieteenlaitos.fi/avoin-data-avattavat-aineistot

import requests

WEATHER_URL = "http://opendata.fmi.fi/wfs/fin?"
storedquery_id = "fmi::observations::weather::multipointcoverage"
place = "Helsinki"
starttime="2000-01-01T00:00:00Z"
endtime="2000-01-05T23:59:59Z"

response = requests.get(WEATHER_URL
                       + "service=WFS&"
                       + "version=2.0.0&"
                       + "request=GetFeature&"
                       + f"storedquery_id={storedquery_id}&"
                       + f"place={place}&"
                       + f"starttime={starttime}&"
                       + f"endtime={endtime}"
                       )
with open(f"../data/weather_data/weather_data.xml", "w") as f:
                f.write(response.text)
