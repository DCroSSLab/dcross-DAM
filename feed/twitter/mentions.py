"""
Project Name: 	DCroSS
Author List: 	Saumyaranjan Parida
Filename: 		mentions.py
Description: 	Gets and stores tweets in which the bot is mentioned using tweepy
"""


from pprint import pprint
from dcross_DAM.config_vars import TWITTER_BOT_USERNAME
from .database_twitter import TwitterDatabase
from .twitter_client import api

"""
User management is not done, like it is done for Telegram.
Every new user is given a unique reporter_id, this identity is then present in
all reports of this user.
"""

db_client = TwitterDatabase()


def get_mentions():
    try:
        mentions = api.mentions_timeline(since_id=db_client.get_since_id(), tweet_mode="extended")
        since_id = mentions[0].id
        db_client.update_since_id(since_id)
        for status in mentions:
            images = []
            description = status.full_text
            if TWITTER_BOT_USERNAME in status.full_text:
                description = status.full_text.replace(TWITTER_BOT_USERNAME, "")
            if "media" in status.entities:
                for image in status.entities["media"]:
                    images.append(image["media_url"])
            db_client.create_twitter_report(status.id, status.user.id, "123", status.user.screen_name,
                                            status.created_at, description, images, status.coordinates,
                                            status.place.bounding_box.coordinates,
                                            "12345")

    except Exception as e:
        print(e)
        return
