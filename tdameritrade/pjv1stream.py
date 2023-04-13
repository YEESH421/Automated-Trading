from streamtweets import *
import tweepy

pjId = '888225282334871553'
tonyId = ""
auth = tweepy.OAuthHandler(config.twitter_api_key1, config.twitter_api_key_secret1)
auth.set_access_token(config.twitter_access_token1, config.twitter_access_token_secret1)
api = tweepy.API(auth)
c = authenticate()
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.text[0] != '@' and status.text.split()[0] != 'RT' and status.in_reply_to_user_id == None:
            print(status.text)
            parseAndBuyPJAlert(status.text, PwaitTime, PpositionSize, c)
    def on_error(self, status_code):
        print(status_code)
        return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=[pjId])
