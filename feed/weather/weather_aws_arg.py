from datetime import datetime, timedelta
from pprint import pprint

import requests

from dcross_DAM.database import DBClient


def extract_numerical_value(phrase, phrase_type: type):
    if phrase == "":
        return None
    else:
        return phrase_type(phrase)


def extract_string_value(phrase):
    if phrase.isupper():
        return phrase.title()
    return phrase


class AwsArgWeatherFeed:
    def __init__(self, client):
        self.client = client
        self.aws_arg_weather = client.events.aws_arg_weather

    def get_weather_feed(self, station_type="ALL", date=datetime.utcnow().strftime("%Y-%m-%d"),
                         utc_hour=(datetime.utcnow()-timedelta(hours=1)).strftime("%H")):
        aws_arg_weather = self.aws_arg_weather
        # station_type = ["ALL", "AWS", "ARG", "AGRO", "AWSAGRO"]
        url = "http://aws.imd.gov.in:8091/AWS/dataonmap.php?a={}&b={}&c={}".format(station_type, date, utc_hour)
        response = requests.get(url)
        # print(type(response.json())) ---> list
        bulk_insert = []
        for item in response.json():
            attributes = item.split(",")
            latitude = float(attributes[0])
            longitude = float(attributes[1])
            station_type = attributes[2]
            # state = attributes[3]
            state = extract_string_value(attributes[3])
            # district = attributes[4]
            district = extract_string_value(attributes[4])
            station = attributes[5]
            # some stations have a trailing space, removing the same
            if station[-1:] == " ":
                station = station[:-1]
            station = extract_string_value(station)
            # temperature in Celsius
            # temperature = float(attributes[6])
            temperature = extract_numerical_value(attributes[6], float)
            # humidity in whole percentages
            # real_humidity = int(attributes[7])
            real_humidity = extract_numerical_value(attributes[7], int)
            # rainfall in millimetres
            # rainfall = float(attributes[8])
            rainfall = extract_numerical_value(attributes[8], float)
            # wind speed in knots (kt)
            # wind_speed = int(attributes[9])
            wind_speed = extract_numerical_value(attributes[9], int)
            # wind direction in degrees
            # wind_direction = int(attributes[10])
            wind_direction = extract_numerical_value(attributes[10], int)
            payload = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                       "properties": {
                           "forecast_type": "AWS ARG Network", "source": "IMD", "station_name": station,
                           "station_type": station_type, "forecast": {
                               "issue_time": datetime.utcnow()-timedelta(hours=1),
                               "state": state, "district": district,
                               "rainfall": {"value": rainfall, "unit": "mm"},
                               "temperature": {"value": temperature, "unit": "C"},
                               "real_humidity": {"value": real_humidity, "unit": "%"},
                               "wind_speed": {"value": wind_speed, "unit": "kt"},
                               "wind_direction": {"value": wind_direction, "unit": "degree"}
                           }
                       }}
            bulk_insert.append(payload)
        aws_arg_weather.insert_many(bulk_insert)


# feed = AwsArgWeatherFeed(DBClient())
# feed.get_weather_feed()
