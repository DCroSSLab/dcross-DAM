"""
Project Name: 	DCroSS
Author List: 	Saumyaranjan Parida
Filename: 		twitter_client.py
Description: 	A tweepy api instance is initialised here
"""


import tweepy
from dcross_DAM.config_vars import \
    TWITTER_CONSUMER_API_KEY, TWITTER_CONSUMER_API_SECRET, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_ACCESS_TOKEN

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_API_KEY, TWITTER_CONSUMER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)