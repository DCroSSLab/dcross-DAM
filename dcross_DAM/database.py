from pymongo import MongoClient

uri = "mongodb://faraaz:winterfell@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"


class DBClient:
    def __init__(self):
        client = MongoClient(uri)
        self.connection = client
        self.events = client.events
        self.users = client.users
        self.reports = client.reports

    def create_twitter_report(self, tweet_id, user_id, reporter_id, username, create_time, description, images, coordinates=None,
                              place=None, disaster_id=None):
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
