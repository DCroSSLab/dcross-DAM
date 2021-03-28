import json
from random import randint

from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from dcross_DAM.celery import tasker
from dcross_DAM.database import DBClient
from .earthquake.earthquake_ncs import NCSEarthquakesFeed
from .weather.weather_imd_nowcast import IMDNowcastFeed
from .weather.weather_aws_arg import AwsArgWeatherFeed


db_client = DBClient()
ncs_earthquakes_feed = NCSEarthquakesFeed(db_client)
imd_nowcast_feed = IMDNowcastFeed(db_client)
aws_arg_feed = AwsArgWeatherFeed(db_client)


@shared_task(name="feed.tasks.operation_add")
def operation_add(x, y):
    print("Performing add operation now")
    print(x+y)


@shared_task(name="feed.tasks.earthquake_ncs")
def earthquake_ncs():
    ncs_earthquakes = ncs_earthquakes_feed.get_ncs_earthquakes()
    ncs_earthquakes_feed.record_ncs_earthquakes(ncs_earthquakes)


@shared_task(name="feed.tasks.nowcast_imd")
def nowcast_imd():
    imd_nowcasts = imd_nowcast_feed.get_imd_nowcasts()


@shared_task(name="feed.tasks.weather_aws_arg")
def weather_aws_arg():
    weather = aws_arg_feed.get_weather_feed()


