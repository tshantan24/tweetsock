from .model import predict
from .models import Handle
from django.shortcuts import render
from django.http import JsonResponse
from tweets.get_tweets import get_tweets
from timeit import default_timer as timer
from tweets.handle_exists import handle_exists, get_keywords, get_hashtags
# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/index.html', context=None)


def getParty(request):

    data = {'msg':0,
    'party': -1,
    'keywords': None,
    'key_pos': None,
    'key_neg': None,
    'total_pos': None,
    'total_neg': None,
    'hashtags': None,
    'hashtag_count': None,}

    if request.method == 'GET':
        hndle = request.GET.get('handle')
        print('Handle: ' + hndle)

        # if handle_exists(hndle):
        #     test = Handle.objects.get(handle = hndle)
        #     data['party'] = test.party
        #     data['msg'] = 1

        # else:
        start_time = timer()
        code, tweets, tweet_objs = get_tweets(hndle)
        end_time = timer()

        print("Time taken to get tweets: " + str(end_time-start_time))
        print()
        print("Length of tweets: {}".format(len(tweets)))
        print()

        if code == -1:
            data['msg'] = -1  #Handle doesn't exist

        elif code == -2:
            data['msg'] = -2 #Tweets are protected and not accessible

        elif code == -3:
            data['msg'] = -3 #Number of tweets is not 100

        elif code == 0:

            start_time2 = timer()
            keywords, pos, neg, total_pos, total_neg = get_keywords(list(tweets))
            top_hashtags, hashcounts = get_hashtags(tweet_objs)
            end_time2 = timer()

            print("Time taken to get stats: " + str(end_time2-start_time2))
            print()

            data['keywords'] = keywords
            data['key_pos'] = pos
            data['key_neg'] = neg
            data['total_pos'] = total_pos
            data['total_neg'] = total_neg
            data['hashtags'] = top_hashtags
            data['hashtag_count'] = hashcounts

            pre_time1 = timer()
            data['party'] = predict(tweets)
            pre_time2 = timer()
            print("Time taken to predict: " + str(pre_time2-pre_time1))
            print()

            if data['party'] == 1:
                data['msg'] == "Republican"

            else:
                data['msg'] == "Democrat"

            # new_handle = Handle(handle=hndle, party=data['party'])
            # new_handle.save()

    return JsonResponse(data)
