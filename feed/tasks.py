"""
Project Name: 	DCroSS
Author List: 	Faraaz Biyabani
Filename: 		tasks.py
Description: 	Celery "feed" tasks
"""


from celery import shared_task
from dcross_DAM.database import DBClient
from .earthquake.earthquake_ncs import NCSEarthquakesFeed
from .weather.weather_imd_nowcast import IMDNowcastFeed
from .weather.weather_aws_arg import AwsArgWeatherFeed
from .twitter.mentions import get_mentions


db_client = DBClient()
ncs_earthquakes_feed = NCSEarthquakesFeed(db_client)
imd_nowcast_feed = IMDNowcastFeed(db_client)
aws_arg_feed = AwsArgWeatherFeed(db_client)


@shared_task(name="feed.tasks.earthquake_ncs")
def earthquake_ncs():
    print("Fetching earthquakes from NCS")
    ncs_earthquakes = ncs_earthquakes_feed.get_ncs_earthquakes()
    ncs_earthquakes_feed.record_ncs_earthquakes(ncs_earthquakes)


@shared_task(name="feed.tasks.nowcast_imd")
def nowcast_imd():
    print("Fetching nowcasts from IMD")
    imd_nowcasts = imd_nowcast_feed.get_imd_nowcasts()


@shared_task(name="feed.tasks.weather_aws_arg")
def weather_aws_arg():
    print("Fetching weather from AWS-ARG Network")
    weather = aws_arg_feed.get_weather_feed()


@shared_task(name="feed.tasks.twitter_mentions")
def twitter_mentions():
    print("Fetching status reports from Twitter")
    mentions = get_mentions()


