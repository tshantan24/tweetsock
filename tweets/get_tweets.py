import re
import tweepy 
import pandas as pd 

consumer_key = "JbhkSllQEEowFT000MRpEDaWq"
consumer_secret = "VoM097AKZtxSBnWvwP8MV39AGOuG1JArHf87wLpRF2L5CMZwF4"
access_key = "1708179600-1jTfBFKcs3uIR4pHAAYC3y2za8051gfs0avFdRY"
access_secret = "B3BOGQ7I45zq4OZWMg6gCFWj794Mjo0U4FrCsynq1y5i4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth) 


def get_tweets(handle):
	try:
		tweet_objs = [tweet for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle, tweet_mode='extended').items(300) if (not tweet.retweeted) and ('RT @' not in tweet.full_text)]
		tweets = [tweet.full_text for tweet in tweet_objs]

	except tweepy.TweepError as e:
		code=re.findall('\d+',e.reason)
		code = int(code[0])
		if code == 404:
			return -1, None, None #if the user does not exist
		elif code == 401:
			return -2, None, None #if tweets are protected and not accessible

	print("Len of tweets: " + str(len(tweets)))
	print()

	if len(tweets)<120:
		return -3, None, None	#if number of tweets is not 100
		
	return 0, pd.Series(tweets), tweet_objs
