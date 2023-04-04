import calendar
import time
import math
from main import buyOption, sellOption

joeBlacklist = set()
f1 = open("joeBlacklist.txt", "r")
for x in f1:
  joeBlacklist.add(x.replace('\n', ''))
f1.close()

# get list of months create a dictionary of months to month number
months = list(calendar.month_abbr)
monthsToDigDic = {month: index for index,
                  month in enumerate(calendar.month_abbr) if month}

def parseAndBuyJoeAlert(tweet, waitTime, money, wb):
    call = False
    put = False
    stock, price, month, day, call, put = scrapeInfov5(tweet)
    if stock == "" or price == "" or month == "" or day == "":
        stock, price, month, day, call, put = scrapeInfov4(tweet)
    if stock != "" and price != "" and month != "" and day != "" and stock not in joeBlacklist:
        stock, expDate, strike = formatv2(stock, price, month, day, call, put)
        quantity = buyOption(stock, expDate, strike, wb, money)
        print("     Joe Option: ", stock, "Buy Time: ",
            time.ctime(time.time()), "Quantity: ", quantity)
        time.sleep(30) #hardcoded time
        quarterQuantity = math.floor(.25 * quantity)
        lastQuarter = quantity - quarterQuantity*3
        if quantity > 0:
            sellOption(stock, expDate, strike, wb, quarterQuantity)
            print("     Joe Option: ", stock, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            sellOption(stock, expDate, strike, wb, quarterQuantity)
            print("     Joe Option: ", stock, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            sellOption(stock, expDate, strike, wb, quarterQuantity)
            print("     Joe Option: ", stock, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  quarterQuantity)
            time.sleep(10) #hardcoded time

            sellOption(stock, lastQuarter, wb)
            print("     Joe Option: ", stock, "Sell Time: ",
                  time.ctime(time.time()), "Quantity: ",  lastQuarter)
        elif quantity == 0:
            print("     Insufficient funds for: ", stock)
        elif quantity == -1:
            print("     Symbol most likely doesn't exist/malformed: ", stock)

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


def scrapeInfov5(tweet):
    stock = ""
    price = ""
    month = ""
    day = ""
    call = False
    put = False
    text = tweet
    text = text.replace(',', '')
    text = text.replace('?', '')
    text = text.replace('!', '')
    words = text.split()
    # we filter out tweets with percentages in them
    conditions = 'moving' not in text.lower() and 'roll' not in text.lower() and 'earlier' not in text.lower() and 'hold' not in text.lower() and 'print' not in text.lower() and ('%' not in text) and ('🔥' not in text) and ('congrat' not in text.lower()) and words[0][0] != '@' and words[0] != 'RT'
    for word in words:
        if word[0] == '$' and len(word) > 1:
            if word[1].isalpha():
                for letter in word:
                    if letter.isalpha():
                        stock += letter
                break
    if conditions and stock:
        if 'calls' in text.lower() and 'puts' not in text.lower():
            call = True
        if 'puts' in text.lower():
            put = True
        l = len(words)
        for i in range(l-5):
            candidate = words[i:i+6]
            hit, labels = containsMonthDayPricev2(candidate)
            if hit:
                priceIndex = labels.index('price')
                monthIndex = labels.index('month')
                dayIndex = labels.index('day')
                price = candidate[priceIndex]
                if candidate[priceIndex][0] == '$':
                    price = candidate[priceIndex][1:]
                month = candidate[monthIndex]
                if month.lower() == 'july':
                    month = 'July'
                else:
                    month = month[0].upper() + month[1:3].lower() 
                day = parseDig(candidate[dayIndex])
    return stock, price, month, day, call, put


def scrapeInfov4(tweet):
    stock = ""
    price = ""
    month = ""
    day = ""
    call = False
    put = False
    text = tweet
    text = text.replace(',', '')
    text = text.replace('?', '')
    words = text.split()
    conditions = 'moving' not in text.lower() and 'roll' not in text.lower() and 'earlier' not in text.lower() and 'hold' not in text.lower() and 'print' not in text.lower() and ('%' not in text) and ('🔥' not in text) and ('congrat' not in text.lower()) and words[0][0] != '@' and words[0] != 'RT'
    if conditions:
        words[0] = words[0].replace('$', '')
        if words[0].isalpha() and words[0].isupper():
            stock = words[0]
        for i in range(1, len(words)):  # this might need to be len(words), haven't checked
            # This is the case where the string contains $"XX" calls--now we definitely have the price
            if 'call' in words[i].lower() and words[i - 1][0] == '$':
                price = words[i - 1].replace('$', '')
                call = True
            # This is the case where the string contains $"XX" calls--now we definitely have the price
            elif 'put' in words[i].lower() and words[i - 1][0] == '$':
                price = words[i - 1].replace('$', '')
                put = True
            elif ismonthDayPricev2(words[i]) == 'month':
                month = words[i]
                if ismonthDayPricev2(words[i-1]) == 'day':
                    day = parseDig(words[i-1])
                if ismonthDayPricev2(words[i+1]) == 'day':
                    day = parseDig(words[i+1])
    return stock, price, month, day, call, put



def formatv2(stock, strike, month, day, call, put):
    monthDig = str(monthsToDigDic[month])
    if len(day) < 2:
        day = '0' + day
    if len(monthDig) < 2:
        monthDig = '0' + monthDig
    if month == 'Nov' or month == 'Dec':
        yr = '2021'
    else:
        yr = '2022'
    expDate =yr+'-'+ monthDig+'-'+day
    strike = strike.replace('$', '')
    return stock, expDate, strike


