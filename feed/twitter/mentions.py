from pprint import pprint

from dcross_DAM.config_vars import TWITTER_BOT_USERNAME
from dcross_DAM.database import DBClient
from twitter_client import api
db_client = DBClient()


def get_mentions():
    try:
        mentions = api.mentions_timeline(since_id=1376131989841932288, tweet_mode="extended")
        for status in mentions:
            images = []
            pprint(status)
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


get_mentions()