import tweepy
import config
from webull import webull
from relogin import *
from mmaparse import *

pin = ''
wb = webull()
relogin(wb)
wb.get_trade_token(pin)

mmaId = '1382530260793581570'
seanId = "1328743715087724546"
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        if status.in_reply_to_user_id == None and status.is_quote_status == False and status.text.split()[0] != 'RT':
            print(status.text)
            segments = status.text.split('\n')
            for s in segments:
                    if s:
                        parseAndBuyMMAAlert(s, 30, 0, wb)                       
    def on_error(self, status_code):
        print(status_code)
stream = MyStreamListener(config.twitter_api_key1, config.twitter_api_key_secret1, config.twitter_access_token1, config.twitter_access_token_secret1)
stream.filter(follow=[seanId])