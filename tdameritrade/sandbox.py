from streamtweets import *
from trade import *
from manzparse import *
from shenobiparse import *
from tda.orders import options
import math
import concurrent.futures
import json


def buySellTest(symbol):
    c = authenticate()
    # buy stock thru Ameritrade right here
    executeBuyOrderOption(symbol, 1, c)
    time.sleep(20)
    executeSellOrderOption(symbol, 1, c)
    # sell stock thru Ameritrade right here
    print("Sell Time: ", time.ctime(time.time()), "Option", symbol)


def loadTweetz(n):
    headers = {"Authorization": "Bearer {}".format(config.bearer_token1)}
    response = requests.get(
        "https://api.twitter.com/labs/2/users/:1200616796295847936", headers=headers)
    return response.json()


def loadTweets(n, id):
    headers = {"Authorization": "Bearer {}".format(config.bearer_token1)}
    response = requests.get(
        "https://api.twitter.com/2/users/"+ id + "/tweets?tweet.fields=created_at,author_id,conversation_id,public_metrics,context_annotations&user.fields=username&expansions=author_id&max_results=" + str(n), headers=headers)
    return response.json()


def printTweets(tweets):
    for tweet in tweets:
        print(tweet['text'] + ' ' + tweet['created_at'])

def stockquotes(c):
    f = open('stocks.txt', 'r')
    for line in f:
        s = line[1:]
        s = s.replace("\n", "")
        print(c.get_quote(s).json()[s]['lastPrice'])
    f.close()


x = {'id': '1339958771276107776',
     'text': '$VERU that dip FireRocket. Goin to take advantage of dips and build my position on the March 19th $25 calls, no ask slapping!'}
y = {"id":"1359334616407146496", "text":"i like beef","author_id":"1319691473185628160"}
#f = {'id': '1339958771276107776', 'text': '$NIO Got out of my calls on spike and moved to Jan 15th 2021 $52 calls on today’s dip for post Jan 2nd delivery report and Jan 9th NIO day run.'}
money = 1000
waitTime = 3
c = authenticate()
stock, strike, month, day, call, put = scrapeInfov5(x['text'])
stk, strk, mnth, dy, cll, pt = scrapeInfov4(x['text'])
#tweets = loadTweets(5, 'Tonald17012110')
Jtweet = '$EDRY All shippers are moving today, EDRY can do a massive breakout here. Goin to get a starter. They have earnings on Tuesday afterhours. Should get interesting Tuesday morning.' 
segments = Jtweet.split('\n')
mt = 'Unusual call option activity leaders this morning Over 65,000 $SNDL 2/19 $5 calls for 85 cents Over 126,000 $DNN 3/19 $2.50 calls for 35 cents Over 6000 $SONO Jan2022 $45 calls for $6.55'
dt = '12/2'
ppp = '$QBAT'
a = formatv2("XLI", "82", "Apr", "16", False, True)
print(a)

#parseAndBuyManzAlert("$SKLZ $26 calls - 28.8% short 👀", 0, 0, c)
#parseAndBuyTTMAlert("Taking $IVR 4.5c 6/18 since Zack is adding more to his position",0,0,c)
x = 'ROOT_Oct1521C7.5'
x = x.upper()
print(x)
print(c.get_quote(x).json())
parseAndBuyJoeAlert("$ROOT that dip FireRocket. Goin to take advantage of dips and build my position on the OCT 15th $7.5 calls, no ask slapping!",0,0,c)
