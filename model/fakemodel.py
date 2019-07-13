import random

def getParty(handle):
    """
        Write code to get 200 tweets of the handle given and check if there are 200 tweets
        Also handle errors to check if the twitter handle exists or not
        If the handle does not exist, then make it return -1 and in Django, show the user an error message saying that
        this user does not exist.

    """
    """
        Fake model of the form

        percentage = predict(tweets)  # This will give the percentage on how likely the handle is a democrat.

        For now this is a dummy function
    """

    percentage = random.uniform(0, 1)
    return percentage