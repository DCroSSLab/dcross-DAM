import ast
import datetime
import json
import re
from pprint import pprint
import pytz
import requests
from bs4 import BeautifulSoup
from dcross_DAM.database import DBClient


def extract_datetime(forecast):
    # cleaning forecast.description and extracting datetime
    forecast["description"] = re.sub(r"\\/", "/", forecast["description"])
    # extracting date and times
    date = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", forecast['description']).group()
    issue_time = date + ' ' + re.search("</br>[0-9]{4} Hrs</br>", forecast['description']).group()[5:9:1]
    expire_time = date + ' ' + re.search("Valid upto: [0-9]{4} Hrs", forecast['description']).group()[12:16:1]
    # Remove all HTML tags, mainly <p>, </p> and </br> are present
    forecast["description"] = re.sub("</?[^><]+>", '', forecast['description'])
    forecast_text = re.sub("( ? Time of issue: .*)", '', forecast["description"])
    # issue_time -----> </br>2200 Hrs</br>  expire_time----->Valid upto: 0100 Hrs
    # print(issue_time, expire_time)
    naive_issue = datetime.datetime.strptime(issue_time, '%Y-%m-%d %H%M')
    naive_expire = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H%M')
    return [naive_issue, naive_expire, forecast_text]


def extract_severity(phrase):
    if phrase == "nowcast_marker\/map-marker-icon-png-yellow.png":
        return "Low"
    elif phrase == "nowcast_marker\/map-marker-icon-png-orange.png":
        return "Medium"
    elif phrase == "nowcast_marker\/map-marker-icon-png-red.png":
        return "High"
    else:
        return None


def extraction(data):
    pattern_images = re.compile(r"(\"images\":\s\[.*]),\s?\nareas\s?:", flags=re.DOTALL)
    data_fixed = re.findall(pattern_images, data)
    cleaned = ast.literal_eval("{" + data_fixed[0] + "}")
    return cleaned
    # print("{" + data_fixed + "}")


class IMDNowcastFeed:
    def __init__(self, client):
        self.conn = client.connection
        self.nowcasts = client.events.nowcasts

    def get_imd_nowcasts(self):
        nowcasts = self.nowcasts
        client = self.conn
        url = 'https://mausam.imd.gov.in/imd_latest/contents/stationwise-nowcast-warning.php'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features='html.parser')
        test = soup.find('script', {'type': 'text/javascript'})
        # print(test.string)
        pattern = re.compile(r"\s+countrydataprovider\s+=\s+(\{.*?\});\n", flags=re.DOTALL)
        data = re.findall(pattern, test.string)
        if data[0]:
            data_cleaned = extraction(data[0])
        else:
            print("Response probably changed from IMD")
            return
        indian = pytz.timezone('Asia/Kolkata')
        for forecast in data_cleaned['images']:
            if forecast['imageURL'] == "nowcast_marker\/map-marker-icon-png-green.png":
                continue
            if forecast['description'] == 'No data Available':
                continue
            severity = extract_severity(forecast['imageURL'])
            station = forecast['title']
            longitude = float(forecast['longitude'])
            latitude = float(forecast['latitude'])
            # noinspection SpellCheckingInspection
            datetimes = extract_datetime(forecast)
            naive_issue, naive_expire, forecast_text = datetimes[0], datetimes[1], datetimes[2]
            issue_time = indian.localize(naive_issue)
            expire_time = indian.localize(naive_expire)
            exists = nowcasts.find_one({'properties.forecast.issue_time': issue_time.astimezone(pytz.utc),
                                        'properties.forecast.expire_time': expire_time.astimezone(pytz.utc),
                                        'properties.station_name': station})
            if exists:
                # print(str(exists["_id"]) + "already exists!")
                continue
            load = {'type': "Feature", 'geometry': {'type': "Point", 'coordinates': [longitude, latitude]},
                    'properties': {'forecast_type': "weather_nowcast", 'source': "IMD",
                                   'station_name': station, 'station_type': "IMD-Station",
                                   'forecast': {'description': forecast_text, 'severity': severity,
                                                'issue_time': issue_time, 'expire_time': expire_time}}}
            nowcasts.insert_one(load)
            # pprint(load)


# feed = IMDNowcastFeed(DBClient())
# feed.get_imd_nowcasts()
