import tweepy
import config
from webull import webull
from relogin import *
from joetweetparse import *

pin = ''
wb = webull()
relogin(wb)
wb.get_trade_token(pin)

joeId = '1047325862675324928'
tonyId = ""
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        if status.in_reply_to_user_id == None:
            print(status.text)
            segments = status.text.split('\n')
            for s in segments:
                    if s:
                        parseAndBuyJoeAlert(s, 40, 300, wb)                        
    def on_error(self, status_code):
        print(status_code)

myStreamListener = MyStreamListener(config.twitter_api_key1, config.twitter_api_key_secret1, config.twitter_access_token1, config.twitter_access_token_secret1)
myStreamListener.filter(follow=[joeId])
