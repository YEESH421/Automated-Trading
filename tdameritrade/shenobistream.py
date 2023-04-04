from streamtweets import *
from shenobiparse import *
import tweepy

ttmId = '1319540410616864769'
tonyId = "1319691473185628160"
auth = tweepy.OAuthHandler(config.twitter_api_key3, config.twitter_api_key_secret3)
auth.set_access_token(config.twitter_access_token3, config.twitter_access_token_secret3)
api = tweepy.API(auth)
c = authenticate()
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.text[0] != '@' and status.text.split()[0] != 'RT' and status.in_reply_to_user_id == None:
            print(status.text)
            segments = status.text.split('\n')
            for s in segments:
                    if s:
                        parseAndBuyTTMAlert(s, JwaitTime, 7000, c)
    def on_error(self, status_code):
        print(status_code)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=[ttmId])
