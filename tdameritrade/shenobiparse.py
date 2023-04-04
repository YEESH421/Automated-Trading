from trade import *
import calendar
from datetime import date
import time
import math
import requests
import config
import json

# tweet parsing functions

# get list of months create a dictionary of months to month number
months = list(calendar.month_abbr)
monthsToDigDic = {month: index for index,
                  month in enumerate(calendar.month_abbr) if month}


def parseDig(x):
    digs = ""
    for i in x:
        if i.isdigit():
            digs += i
    return digs

def containsMonthDayPricev2(candidates):
    hit = False
    labels = ['', '', '', '', '', '']
    for i in range(6):
        x = ismonthDayPricev2(candidates[i])
        if x == 'month':
            labels[i] = x
            if i != 0:
                if candidates[i-1][0].isdigit():
                    labels[i-1] = 'day'
            if i != 5:
                if candidates[i+1][0].isdigit():
                    labels[i+1] = 'day'
        elif x == 'price' or (candidates[i][0].isdigit() and 'day' in labels and labels[i] != 'day') or (candidates[i][0].isdigit() and 'day'  not in labels and 'month' not in labels):
            labels[i] = 'price'
    if 'price' in labels and 'month' in labels and 'day' in labels:
        hit = True
    return hit, labels


def ismonthDayPricev2(x):
    if x[0] == '$' and x[1].isdigit():
        return "price"
    elif x[0].isalpha:
        fx = x[0].upper() + x[1:3].lower()
        if fx in monthsToDigDic:
            return 'month'
    elif x[0].isdigit():
        return "day"
    else:
        return x

# Function for extracting option call details
# 1 see if tweet starts with symbol
# 2 see if tweet contains 3 gram sequences of month, day, price in any order
# Also filter out retweets and replies


def scrapeInfo(tweet):
    call = False
    put = False
    stock = ""
    price = ""
    month = ""
    day = ""
    text = tweet.lower()
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace(',', "")
    words = text.split()
    # we filter out tweets with percentages in them
    conditions = 'moving' not in text.lower() and 'roll' not in text.lower() and 'earlier' not in text.lower() and 'hold' not in text.lower() and 'print' not in text.lower() and ('%' not in text) and ('🔥' not in text) and ('congrat' not in text.lower()) and words[0][0] != '@' and words[0] != 'RT'
    for i in range(len(words)):
        if len(words[i]) > 1:
            if words[i][0] == '$' and words[i][1].isalpha():
                stock = words[i].replace("$", "").upper()
                x = words[i+1] 
                price = x[:-1]
                if x[-1] == 'p':
                    put = True
                else:
                    call = True
                y = words[i+2].split("/")
                month = y[0]
                day = y[1]



    return stock, price, month, day, call, put

def formatv2(stock, strike, month, day, call, put):
    l = 'C'
    if put:
        l = 'P'
    if len(day) < 2:
        day = '0' + day
    if len(month) < 2:
        month = '0' + month
    if month == 'Dec':
        yr = '20'
    else:
        yr = '21'
    strike = strike.replace('$', '')
    if '.' in strike:
        if len(strike.split('.')[1]) > 1:
            if strike[-1] == '0':
                strike = strike[0:-1]
    return stock + '_' + month + day + yr + l + strike


def determineQuantityO(m, c, symbol):
    quantity = -1
    quote = c.get_quote(symbol).json()
    contractPrice = quote[symbol]['askPrice'] * 100
    if contractPrice > 0:  # avoid division by 0
        quantity = int(m//contractPrice)
    return quantity

# remember to change hardcoded holdtimes and positions
def parseAndBuyTTMAlert(tweet, waitTime, money, c):
    call = False
    put = False
    stock, price, month, day, call, put = scrapeInfo(tweet)
    if stock != "" and price != "" and month != "" and day != "":
        symbol = formatv2(stock, price, month, day, call, put)
        quantity = determineQuantityO(money, c, symbol)
        thirdQuantity = math.floor(.33 * quantity)
        if quantity > 0:
            executeBuyOrderOption(symbol, quantity, c)
            print("     TTM Option: ", symbol, "Buy Time: ",
                  time.ctime(time.time()), "Quantity: ", quantity)
            time.sleep(90) #hardcoded time

            executeSellOrderOption(symbol, thirdQuantity, c)
            print("     TTM Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  thirdQuantity)
            time.sleep(30) #hardcoded time

            executeSellOrderOption(symbol, thirdQuantity, c)
            print("     manz Option: ", symbol, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  thirdQuantity)

        elif quantity == 0:
            print("     Insufficient funds for: ", symbol)
        elif quantity == -1:
            print("     Symbol most likely doesn't exist/malformed: ", symbol)