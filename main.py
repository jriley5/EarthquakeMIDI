import json
import requests
import datetime
from midi import quakes_to_midi


# https://earthquake.usgs.gov/fdsnws/event/1/ api info here
# uses unix epoch time in ms

class EarthQuake:
    def __init__(self, time, mag, rms, dmin, lat, long, z, title, url):
        self.url = url
        self.long = long
        self.lat = lat
        self.dmin = dmin
        self.rms = rms
        self.title = title
        self.z = z
        self.mag = mag
        self.time = time


# PARAMS
start = "2022-05-01"
end = "2022-05-15"


# calculate ms during day window
# (not using this anymore)
def calculate_duration_ms(start_time, end_time):
    start_date = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d")

    start_unix_ms = datetime.datetime.timestamp(start_date)
    end_unix_ms = datetime.datetime.timestamp(end_date)
    duration_ms = end_unix_ms - start_unix_ms
    return duration_ms


# returns list of earthquake objects
def collect_earthquakes(start_time, end_time):
    parameters = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "latitude": 0,
        "longitude": 0,
        "maxradiuskm": 20000
    }

    response = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query", params=parameters)
    features = response.json()['features']

    earthquakes = []

    with open('json_data.json', 'w') as outfile:
        json.dump(features, outfile, indent=4)

    for f in features:
        p = f["properties"]

        if p["type"] != "earthquake":
            pass

        mag = p["mag"]
        time = p["time"]
        dmin = p["dmin"]
        rms = p["rms"]
        title = p["title"]
        url = p["url"]

        geometry = f["geometry"]
        lat = geometry["coordinates"][0]
        long = geometry["coordinates"][0]
        z = geometry["coordinates"][0]

        earthquakes += [EarthQuake(time, mag, rms, dmin, lat, long, z, title, url)]
    return earthquakes


quakes = collect_earthquakes(start, end)
# sort quakes by time they occurred
quakes.sort(key=lambda x: x.time)

# this function handles the MIDI conversion and saving .mid file
quakes_to_midi(quakes)

print("Finished! MIDI file available in this folder.")