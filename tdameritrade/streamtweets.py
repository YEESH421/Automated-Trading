from trade import *
from joetweetparse import *
import calendar
import datetime
import time
import requests
import config
import json
import math


JwaitTime = 55
JpositionSize = 5000
RwaitTime = 60
RpositionSize = 25000
CwaitTime = 60
CpositionSize = 25000
ZwaitTime = 60
ZpositionSize = 25000
SwaitTime = 60
SpositionSize = 25000
MwaitTime = 60
MpositionSize = 5000
PwaitTime = 60
PpositionSize = 1000

joeBlacklist = set()
f1 = open("joeBlacklist.txt", "r")
for x in f1:
  joeBlacklist.add(x.replace('\n', ''))
f1.close()

PJBlacklist = set()
ZackBlacklist = set()
StewBlacklist = set()
RipBlacklist = set()
MeadeBlacklist = set()


# remember to change hardcoded holdtimes and positions
def parseAndBuyJoeAlert(tweet, waitTime, money, c):
    call = False
    put = False
    stock, price, month, day, call, put = scrapeInfov5(tweet)
    pennyStock = ''#parsePennyStock(tweet)
    if stock == "" or price == "" or month == "" or day == "":
        stock, price, month, day, call, put = scrapeInfov4(tweet)
    if stock != "" and price != "" and month != "" and day != "" and stock not in joeBlacklist:
        symbol = formatv2(stock, price, month, day, call, put)
        quantity = determineQuantityO(money, c, symbol)
        quarterQuantity = math.floor(.25 * quantity)
        lastQuarter = quantity - quarterQuantity*3
        if quantity > 0:
            joeBlacklist.add(stock)
            executeBuyOrderOption(symbol, quantity, c)
            print("     Joe Option: ", symbol, "Buy Time: ",
                  time.ctime(time.time()), "Quantity: ", quantity)
            time.sleep(40) #hardcoded time

            executeSellOrderOption(symbol, quarterQuantity, c)
            print("     Joe Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            executeSellOrderOption(symbol, quarterQuantity, c)
            print("     Joe Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            executeSellOrderOption(symbol, quarterQuantity, c)
            print("     Joe Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            executeSellOrderOption(symbol, lastQuarter, c)
            print("     Joe Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  lastQuarter)
        elif quantity == 0:
            print("     Insufficient funds for: ", symbol)
        elif quantity == -1:
            print("     Symbol most likely doesn't exist/malformed: ", symbol)
    elif pennyStock and pennyStock not in joeBlacklist:
        price = c.get_quote(pennyStock).json()[pennyStock]['askPrice']
        if price <= 15:
            quantity = determineQuantityE(math.floor(money/2), c, pennyStock)
            if quantity > 0:
                joeBlacklist.add(pennyStock)
                executeBuyOrderEquity(pennyStock, quantity, c)
                print("     Joe Penny: ", pennyStock, "Buy Time: ",
                      time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(waitTime)
                executeSellOrderEquity(pennyStock, quantity, c)
                print("     Joe Penny: ", pennyStock, "Sell Time: ",
                      time.ctime(time.time()), "Quantity: ", quantity)
            elif quantity == 0:
                print("     Insufficient funds for: ", pennyStock)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", pennyStock)


def parseAndBuyZackAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.lower()
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace(',', "")
    text = text.replace('.', "")
    words = text.split()
    ticker = ''
    for word in words:
        if word[0] == '$' and len(word) > 1:
            if word[1].isalpha():
                for letter in word:
                    if letter.isalpha():
                        ticker += letter
                ticker = ticker.upper()
                break
    containsKeywords = "swing" in text or "dip" in text or "add" in text or "entry" in text or "discount" in text or "cheap" in text or "buy" in text or "patience" in text or "paytience" in text or "join" in text
    if 'fda' in text or 'clinical' in text or 'approval' in text:
        money = 5000
    if ticker and containsKeywords and words[0][0] != '@' and words[0] != 'rt' and ticker not in ZackBlacklist:
        marketCap = getMarketCap(ticker)
        if marketCap < 10000:
            quantity = determineQuantityE(money, c, ticker)
            if quantity > 0:
                ZackBlacklist.add(ticker)
                executeBuyOrderEquity(ticker, quantity, c)
                print("     Zack Equity: ", ticker, "Buy Time: ",
                      time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(waitTime)
                executeSellOrderEquity(ticker, quantity, c)
                print("     Zack Equity: ", ticker, "Sell Time: ",
                      time.ctime(time.time()), "Quantity: ",  quantity)
            elif quantity == 0:
                print("     Insufficient funds for: ", ticker)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", ticker)


def parseAndBuyStewieAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.lower()
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace(',', "")
    text = text.replace('.', "")
    words = text.split()
    ticker = ''
    for word in words:
        if word[0] == '$' and len(word) > 1:
            if word[1].isalpha():
                for letter in word:
                    if letter.isalpha():
                        ticker += letter
                ticker = ticker.upper()
                break
    if ('target' in text or 'breakout' in text or 'love' in text) and ticker and words[0][0] != '@' and words[0] != 'rt' and 'got out' not in text and 'exit' not in text and 'close' not in text and ticker not in StewBlacklist:
        marketCap = getMarketCap(ticker)
        if marketCap < 15000:
            quantity = determineQuantityE(money, c, ticker)
            if quantity > 0:
                StewBlacklist.add(ticker)
                executeBuyOrderEquity(ticker, quantity, c)
                print("     Stew Equity: ", ticker, "Buy Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(waitTime)
                executeSellOrderEquity(ticker,  math.floor(.75 * quantity), c)
                print("     Stew Equity: ", ticker, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", math.floor(.75 * quantity))
                time.sleep(30)
                executeSellOrderEquity(ticker, quantity - math.floor(.75 * quantity), c)
                print("     Zack Equity: ", ticker, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity - math.floor(.75 * quantity))
            elif quantity == 0:
                print("     Insufficient funds for: ", ticker)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", ticker)

# Positions and holdtimes are hardcoded, so don't forget to change them when necessary


def parseAndBuyRipsterAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace(',', "")
    text = text.replace('.', "")
    text = text.lower()
    if text.split()[0][0] == '$' and text.split()[0][1].isalpha() and '#addalert' in text and '#update' not in text and '#winner' not in text:
        symbol = text.split()[0][1:].upper()
        marketCap = getMarketCap(symbol)
        quantity = determineQuantityE(money, c, symbol)
        if marketCap < 10000 and symbol not in RipBlacklist:
            if quantity > 0:
                RipBlacklist.add(symbol)
                executeBuyOrderEquity(symbol, quantity, c)
                print("     Rip Equity: ", symbol, "Buy Time: ",
                      time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(waitTime)
                executeSellOrderEquity(symbol, quantity, c)
                print("     Rip Equity: ", symbol, "Sell Time: ",
                      time.ctime(time.time()), "Quantity: ", quantity)
            elif quantity == 0:
                print("     Insufficient funds for: ", symbol)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", symbol)


def parseAndBuyChamathAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace('?', "")
    text = text.replace(',', "")
    text = text.replace('.', "")
    words = text.split()
    buy = False
    symbol = ''
    if words[0] != 'rt' and words[0][0] != '@':
        for word in words:
            if word[0] == '$' and len(word) > 1:
                if word[1].isalpha():
                    symbol = word[1:]
                    buy = True
                break
    if buy:
        quantity = determineQuantityE(money, c, symbol)
        if quantity > 0:
            executeBuyOrderEquity(symbol, quantity, c)
            print("     Chamath Equity: ", symbol, "Buy Time: ",
                  time.ctime(time.time()), "Quantity: ", quantity)
            time.sleep(waitTime)
            executeSellOrderEquity(symbol, quantity, c)
            print("     Chamath Equity: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ", quantity)
        elif quantity == 0:
            print("     Insufficient funds for: ", symbol)
        elif quantity == -1:
            print("     Symbol most likely doesn't exist/malformed: ", symbol)

def parseAndBuyMeadeAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace('?', "")
    text = text.replace(',', "")
    words = text.split()
    buy = False
    symbol = ''
    conditions = ('insider' in text.lower() or 'institutional' in text.lower() or 'buy' in text.lower() or 'cheap' in text.lower() or 'leader' in text.lower() or 'position' in text.lower() or 'lotto' in text.lower() or 'unusual' in text.lower() or 'monster' in text.lower()) and 'boom' not in text.lower() and 'wow' not in text.lower()
    if words[0] != 'rt' and words[0][0] != '@':
        for word in words:
            if word[0] == '$' and len(word) > 1:
                if word[1].isalpha():
                    symbol = word[1:]
                    buy = True
                break
    if buy and conditions and symbol not in MeadeBlacklist:
        MeadeBlacklist.add(symbol)
        if 'calls' in words:
            i = words.index('calls')
            strike = words[i-1]
            date = words[i-2]
            md = date.split('/')
            month = md[0]
            day = md[1]
            if len(day) < 2:
                day = '0' + day
            if len(month) < 2:
                month = '0' + month
            strike = strike.replace('$', '')
            if '.' in strike:
                if len(strike.split('.')[1]) > 1:
                    if strike[-1] == '0':
                        strike = strike[0:-1]
            call = symbol + '_' + month + day + '21' + 'C' + strike
            quantity = determineQuantityO(money, c, call)
            if quantity > 0:
                executeBuyOrderOption(call, quantity, c)
                print("     Meade Option: ", call, "Buy Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(60)

                executeSellOrderOption(call, math.floor(quantity/3), c)
                print("     Meade Option: ", call, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                time.sleep(30)

                executeSellOrderOption(call, math.floor(quantity/3), c)
                print("     Meade Option: ", call, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                time.sleep(30)

                executeSellOrderOption(call, quantity - 2*math.floor(quantity/3), c)
                print("     Meade Option: ", symbol, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity - 2*math.floor(quantity/3))
            elif quantity == 0:
                print("     Insufficient funds for: ", call)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", call)
        else:
            marketCap = getMarketCap(symbol)
            if marketCap < 10000:
                quantity = determineQuantityE(money, c, symbol)
                if quantity > 0:
                    executeBuyOrderEquity(symbol, quantity, c)
                    print("     Meade Equity: ", symbol, "Buy Time: ",
                        time.ctime(time.time()), "Quantity: ", quantity)
                    time.sleep(60)

                    executeSellOrderEquity(symbol, math.floor(quantity/3), c)
                    print("     Meade Equity: ", symbol, "Sell Time: ",
                        time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                    time.sleep(30)

                    executeSellOrderEquity(symbol, math.floor(quantity/3), c)
                    print("     Meade Equity: ", symbol, "Sell Time: ",
                        time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                    time.sleep(30)

                    executeSellOrderEquity(symbol, quantity - 2*math.floor(quantity/3), c)
                    print("     Meade Equity: ", symbol, "Sell Time: ",
                        time.ctime(time.time()), "Quantity: ", quantity - 2*math.floor(quantity/3))
                elif quantity == 0:
                    print("     Insufficient funds for: ", symbol)
                elif quantity == -1:
                    print("     Symbol most likely doesn't exist/malformed: ", symbol)

def parseAndBuyPJAlert(tweet, waitTime, money, c):
    text = tweet
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace('?', "")
    text = text.replace(',', "")
    text = text.replace('.', "")
    words = text.split()
    buy = False
    symbol = ''
    conditions = 'add' in text.lower() or 'dip' in text.lower() or 'here' in text.lower()
    if words[0] != 'rt' and words[0][0] != '@':
        for word in words:
            if word[0] == '$' and len(word) > 1:
                if word[1].isalpha():
                    symbol = word[1:]
                    buy = True
                break
    if buy and conditions and symbol not in PJBlacklist:
        marketCap = getMarketCap(symbol)
        if marketCap < 10000:
            quantity = determineQuantityE(money, c, symbol)
            if quantity > 0:
                PJBlacklist.add(symbol)
                executeBuyOrderEquity(symbol, quantity, c)
                print("     PJ Equity: ", symbol, "Buy Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity)
                time.sleep(60)

                executeSellOrderEquity(symbol, math.floor(quantity/3), c)
                print("     PJ Equity: ", symbol, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                time.sleep(30)

                executeSellOrderEquity(symbol, math.floor(quantity/3), c)
                print("     PJ Equity: ", symbol, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", math.floor(quantity/3))
                time.sleep(30)

                executeSellOrderEquity(symbol, quantity - 2*math.floor(quantity/3), c)
                print("     PJ Equity: ", symbol, "Sell Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity - 2*math.floor(quantity/3))
            elif quantity == 0:
                print("     Insufficient funds for: ", symbol)
            elif quantity == -1:
                print("     Symbol most likely doesn't exist/malformed: ", symbol)

def consumeResponse(response_line, c):
    if response_line:
        data = json.loads(response_line)
        tweet = ''
        if 'data' in data:
            tweet = data['data']
            print('Time: ', time.ctime(time.time()), 'Tweet: ', tweet)
        elif 'text' in data:
            tweet = data['text']
            print('Time: ', time.ctime(time.time()), 'Tweet: ', tweet)
        else:
            print('Time: ', time.ctime(time.time()), 'Data: ', data)
        if tweet['author_id'] == '1319540410616864769' and "in_reply_to_user_id" not in tweet.keys():
            segments = tweet['text'].split('\n')    
            for s in segments:
                if s:           
                    parseAndBuyTTMAlert(s, SwaitTime, 500, c)
        if tweet['author_id'] == '1047325862675324928' and "in_reply_to_user_id" not in tweet.keys():
            segments = tweet['text'].split('\n')
            for s in segments:
                if s:
                    parseAndBuyJoeAlert(s, SwaitTime, SpositionSize, c)
        if tweet['author_id'] == '1054561163843751936'  and "in_reply_to_user_id" not in tweet.keys():
            parseAndBuyRipsterAlert(tweet['text'], RwaitTime, RpositionSize, c)
        if tweet['author_id'] == '3291691' and "in_reply_to_user_id" not in tweet.keys():
            parseAndBuyChamathAlert(tweet['text'], CwaitTime, CpositionSize, c)
        if tweet['author_id'] == '373620043' and "in_reply_to_user_id" not in tweet.keys():
            parseAndBuyZackAlert(tweet, ZwaitTime, ZpositionSize, c)
        if tweet['author_id'] == '52166809' and "in_reply_to_user_id" not in tweet.keys():
            parseAndBuyStewieAlert(tweet['text'], SwaitTime, SpositionSize, c)
        if tweet['author_id'] == '758386485846544384' and "in_reply_to_user_id" not in tweet.keys():
            parseAndBuyMeadeAlert(tweet['text'], MwaitTime, MpositionSize, c)
        


# twitter stream setup

def create_headers(bearer_token1):
    headers = {"Authorization": "Bearer {}".format(bearer_token1)}
    return headers


def get_rules(headers, bearer_token1):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    print('old rules', json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token1, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print('status on deleting old rules', json.dumps(response.json()))


def set_rules(headers, delete, bearer_token1, new_rules):
    # You can adjust the rules if needed
    payload = {"add": new_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    print('new rules', json.dumps(response.json()))


def get_stream(headers, set, bearer_token1, c):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=in_reply_to_user_id,author_id", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        data = {}
        if response_line:
            data = json.loads(response_line)
        if 'errors' not in data:
            try:
                consumeResponse(response_line, c)
            except:
                print(response_line, " Failed doing something bruh")
        else:
            get_stream(headers, set, bearer_token1, c)


def main():
    # set rules on what tweets to scrape
    rules = [
        {"value": "from:shinobisignals"}]
    test_rules1 = [
        {"value": "(from:IncomingHardo) OR from:ripster47 OR from: Tonald17012110"}]
    test_rules2 = [{"value": "ohio state"}]

    c = authenticate()
    # setup for subscribing to tweet stream
    headers = create_headers(config.bearer_token1)
    old_rules = get_rules(headers, config.bearer_token1)
    delete = delete_all_rules(headers, config.bearer_token1, old_rules)
    set = set_rules(headers, delete, config.bearer_token1, rules)
    get_stream(headers, set, config.bearer_token1, c)


if __name__ == "__main__":
    main()
