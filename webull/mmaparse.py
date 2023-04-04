import calendar
import time
import math
from main import buyOption, sellOption

def parseAndBuyMMAAlert(tweet, waitTime, psize, wb):
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
    conditions = words[0][0] != '@' and words[0] != 'rt' and 'calls' in text and 'exp' in text and 'watching' not in text
    if conditions:
        for word in words:
            if word[0] == '$' and len(word) > 1:
                if word[1].isalpha():
                    for letter in word:
                        if letter.isalpha():
                            stock += letter
                            stock = stock.upper()
                    break
        strikeIndex = words.index("calls") - 1
        if 'exp.' in words:
            dateIndex = words.index("exp.") + 1   
        else:
            dateIndex = words.index("exp") + 1    
        strike = words[strikeIndex]
        strike = strike.replace('$', '')
        date = words[dateIndex].split('/')
        month = date[0]
        day = date[1]
        if len(month) < 2:
            month = '0' + month
        if len(day) < 2:
            day = '0' + day
        year = '2022'
        if month == '11' or month == '12':
            year = '2021'
        expDate = year+'-'+ month+'-'+day
        print(strike,stock,expDate)
        f = open('blacklist.txt', 'r')
        if stock not in f.read():
            f.close()
            f = open('blacklist.txt', 'a+')
            f.write(stock + '\n')
            f.close()
            quantity, spread, bought, askPrice = buyOption(stock, expDate, strike, wb, psize, True)
            if bought:
                print("     mma Option: ", stock, "Buy Time: ",
                    time.ctime(time.time()), "Quantity: ", quantity)
                partialQuantity = quantity//3
                remainder = quantity - 2*partialQuantity          
                time.sleep(30)
                sellOption(stock, expDate, strike, wb, partialQuantity)
                print("     mma Option: ", stock, "sell Time: ",
                time.ctime(time.time()), "Quantity: ", partialQuantity)  
                time.sleep(15)
                sellOption(stock, expDate, strike, wb, partialQuantity)
                print("     mma Option: ", stock, "sell Time: ",
                time.ctime(time.time()), "Quantity: ", partialQuantity)
                sellOption(stock, expDate, strike, wb, remainder)
                print("     mma Option: ", stock, "sell Time: ",
                time.ctime(time.time()), "Quantity: ", remainder) 
            else:
                print('       mma Option not bought: ' + stock + expDate + strike)