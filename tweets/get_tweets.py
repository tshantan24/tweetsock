import pandas as pd 
import numpy as np 
import tweepy 
import re

consumer_key = "JbhkSllQEEowFT000MRpEDaWq"
consumer_secret = "VoM097AKZtxSBnWvwP8MV39AGOuG1JArHf87wLpRF2L5CMZwF4"
access_key = "1708179600-1jTfBFKcs3uIR4pHAAYC3y2za8051gfs0avFdRY"
access_secret = "B3BOGQ7I45zq4OZWMg6gCFWj794Mjo0U4FrCsynq1y5i4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth) 

def get_tweets(handle):
	try:
		tweets = [tweet.full_text for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle, tweet_mode='extended').items(500) if (not tweet.retweeted) and ('RT @' not in tweet.full_text)]
	except tweepy.TweepError as e:
		code=re.findall('\d+',e.reason)
		code = int(code[0])
		if code == 404:
			return -1
		elif code == 401:
			return -2
	if len(tweets)<200:
		return -3	
		
	return tweets
