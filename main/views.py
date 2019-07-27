from timeit import default_timer as timer
from .model import predict 
from .models import Handle
from tweets.get_tweets import get_tweets
from tweets.handle_exists import handle_exists
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/index.html', context=None)


def getParty(request):

    data = {'msg': 0, 'party': -1}

    if request.method == 'GET':
        hndle = request.GET.get('handle')
        print('Handle: ' + hndle)

        if handle_exists(hndle):
            test = Handle.objects.get(handle = hndle)
            data['party'] = test.party
            data['msg'] = 1

        else:
            start_time = timer()
            code, tweets = get_tweets(hndle)
            end_time = timer()

            print("Time to get tweets: " + str(end_time-start_time))
            if code == -1:
                data['msg'] = -1  #Handle doesn't exist
            
            elif code == -2:
                data['msg'] = -2 #Tweets are protected and not accessible
            
            elif code == -3:
                data['msg'] = -3 #Number of tweets is not 100

            elif code == 0:
                pre_time1 = timer()
                data['party'] = predict(tweets)
                pre_time2 = timer()
                print("Time taken to predict: " + str(pre_time2-pre_time1))

                if data['party'] == 1:
                    data['msg'] == "Republican"
            
                else:
                    data['msg'] == "Democrat"

                new_handle = Handle(handle=hndle, party=data['party'])
                new_handle.save()

    return JsonResponse(data)
