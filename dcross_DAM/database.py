"""
Project Name: 	DCroSS
Author List: 	Faraaz Biyabani
Filename: 		database.py
Description: 	Database connection
"""

from pymongo import MongoClient

uri = "mongodb://faraaz:winterfell@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"


class DBClient:
    def __init__(self):
        client = MongoClient(uri)
        self.connection = client
        self.events = client.events
        self.users = client.users
        self.reports = client.reports
        self.dcross = client.dcross
