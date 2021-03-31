"""
Project Name: 	DCroSS
Author List: 	Saumyaranjan Parida
Filename: 		database_twitter.py
Description: 	Database utility functions for Twitter Feed
"""


from dcross_DAM.database import DBClient


class TwitterDatabase:
    def __init__(self):
        client = DBClient()
        self.connection = client
        self.users = client.users
        self.reports = client.reports
        self.dcross = client.dcross

    def update_since_id(self, new_id):
        dcross = self.dcross
        result = dcross.variables.update_one({"platform": "Twitter"}, {"$set": {"last_fetched_mention": new_id}})
        if result:
            return True
        else:
            return False

    def get_since_id(self):
        dcross = self.dcross
        result = dcross.variables.find_one({"platform": "Twitter"})
        if result:
            return result["last_fetched_mention"]

    def create_twitter_report(self, tweet_id, user_id, reporter_id, username, create_time, description, images,
                              coordinates=None, place=None, disaster_id=None):
        twitter_reports = self.reports.twitter
        report = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": place
            },
            "properties": {
                "reporter_id": reporter_id,
                "source": {
                    "platform": "Twitter",
                    "user_id": user_id,
                    "username": username,
                    "tweet_id": tweet_id
                },
                "disaster": {
                    "type": "earthquake",
                    "_id": disaster_id
                },
                "time": create_time,
                "description": {
                    "text": description,
                    "images": images,
                },
                "is_spam": False,
                "is_removed": False
            }
        }
        print(report)
        result = twitter_reports.insert_one(report)
