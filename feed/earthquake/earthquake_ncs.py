"""
Project Name: 	DCroSS
Author List: 	Faraaz Biyabani
Filename: 		earthquake_ncs.py
Description: 	Extracts earthquakes from NCS website
"""


import datetime
import json
import re
from pprint import pprint
import pytz
import requests
from bs4 import BeautifulSoup
from bson.json_util import loads

NCS_MIN_IMPACT_MAGNITUDE = 5.5


class NCSEarthquakesFeed:
    def __init__(self, client):
        self.conn = client
        self.earthquakes = client.events.earthquakes
        # self.earthquakes = client.events.earthquakes
        # self.hello = "hello"

    def get_ncs_earthquakes(self, region: str = "I", north: str = "", west: str = "", east: str = "",
                            south: str = "", latitude: str = "", longitude: str = "", distance: str = "",
                            days: str = "1", start_date: str = "", end_date: str = "", mag_min: str = "0",
                            mag_max: str = "10", depth_min: str = "0", depth_max: str = "1000",
                            timezone: str = "IST"):
        url = "https://seismo.gov.in/MIS/riseq/earthquake"
        if timezone != "IST" and timezone != "UTC":
            return None
        while days not in ({"", "1", "7", "30"}):
            return None
        if north and west and south and east != "":
            region = "C"
        if start_date and end_date != "":
            days = "C"
        if timezone == "IST":
            timezone = "2"
        elif timezone == "UTC":
            timezone = "1"
        parameters = {
            "region": region,
            "region_lat_2": north,
            "region_long_1": west,
            "region_long_2": east,
            "region_lat_1": south,
            "point_lat": latitude,
            "point_long": longitude,
            "point_distance": distance,
            "days": days,
            "start_time": start_date,
            "end_time": end_date,
            "magnitude-min": mag_min,
            "magnitude-max": mag_max,
            "depth-min": depth_min,
            "depth-max": depth_max,
            "timezone": timezone,
            "submit": "Apply"
        }
        page = requests.post(url, data=parameters)
        juice = BeautifulSoup(page.content, 'html.parser')
        data = juice.find_all('li', 'list-view-item event_list')
        earthquakes = [loads(item.attrs.get('data-json')) for item in data]
        return earthquakes

    def record_ncs_earthquakes(self, earthquakes):
        earthquakes_db = self.earthquakes
        indian = pytz.timezone('Asia/Kolkata')
        for earthquake in earthquakes:
            event_id = earthquake['event_id']
            exists = earthquakes_db.find_one({'properties.ncs_id': event_id})
            if exists:
                print(event_id + "exists")
                continue
            naive = datetime.datetime.strptime(earthquake['origin_time'][:19], '%Y-%m-%d %H:%M:%S')
            time = indian.localize(naive)
            lat_long = earthquake['lat_long'].split(', ')
            latitude = float(lat_long[0])
            longitude = float(lat_long[1])
            mag_depth = earthquake['magnitude_depth']
            magnitude = float(re.search(r"\d+\.?\d*", mag_depth).group())
            # if magnitude >= NCS_MIN_IMPACT_MAGNITUDE:
            #     # send periodic task to scheduler backend
            #     return
            depth = float(re.search(r"(\d*\.?\d*)km", mag_depth).group(1))
            name = re.sub(r'M:\s(\d+\.\d+)\s-\s', '', earthquake['event_name'])
            event = dict(type="Feature", geometry=dict(type="Point", coordinates=[longitude, latitude]),
                         properties=dict(disaster_type="earthquake", time=time, name=name,
                                         magnitude=float(magnitude), depth=dict(value=depth, unit="km"),
                                         total_reports=0, reports=[], source="NCS", ncs_id=event_id))
            earthquakes_db.insert_one(event)


# feed = NCSEarthquakesFeed(DBClient())
# earthquakes = feed.get_ncs_earthquakes(days="30")
# feed.record_ncs_earthquakes(earthquakes)
