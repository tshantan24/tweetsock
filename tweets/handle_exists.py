from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from tweets import get_tweets
from main.models import handles
from textblob import TextBlob
from rake_nltk import Rake, Metric
import re
from collections import Counter



def handle_exists(handle):
    list_of_handles_raw = list(handles.objects.values('handle'))
    list_of_handles = []
    x = False
    for i in range(len(list_of_handles_raw)):
        list_of_handles.append(list_of_handles_raw[i]['handle'])
    if handle in list_of_handles:
        x = True
    return x

def get_keywords(tweets):
    pos = 0
    neg = 0
    for c in tweets:
        polarity = TextBlob(c).sentiment.polarity
        if polarity >= 0:
            pos += 1
        elif polarity <= 0:
            neg += 1
    total_string = " ".join(tweets)
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY,max_length=2)
    words = r.extract_keywords_from_text(total_string)
    words1 = r.get_ranked_phrases()
    words2 = words1[:5]
    words3 = []
    occ = 0
    keywords = []
    positive = []
    negetive = []
    for t in words2:
        s = t.strip('\ ’')
        words3.append(s)
    for x in words3:
        pos1=0
        neg1=0

        for t in tweets:
            t = t.lower()
            if x in t:
                polarity1 = TextBlob(t).sentiment.polarity
                if polarity1 >= 0:
                    pos1 += 1
                elif polarity1 <= 0:
                    neg1 += 1
        keywords.append(x)
        positive.append(pos1)
        negetive.append(neg1)
    return keywords,positive,negetive,pos,neg

def get_hashtags(tweets):
    hash = []
    for t in tweets:
        hash.append(t.entities.get('hashtags'))
    hash1= [hash2 for hash2 in hash if hash2 != []]
    hash3 = []
    for f in range(0,len(hash1)):
        for d in range(0,len(hash1[f])):
            hash3.append(hash1[f][d]['text'])
    counts = Counter(hash3)
    finalhash = counts.most_common(5)
    onlyhash = [item[0] for item in finalhash]
    onlycounts = [item[1] for item in finalhash]
    return onlyhash,onlycounts
