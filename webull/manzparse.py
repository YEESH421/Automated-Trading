import time
import calendar
from main import buyOption, sellOption

def parseAndBuyManzAlert(tweet, waitTime, psize, wb):
    call = None
    stock = ""
    strike = ""
    month = ""
    day = ""
    text = tweet.lower()
    text = text.replace('\n', " ")
    text = text.replace('!', "")
    text = text.replace(',', "")
    words = text.split()
    conditions = 'high' in text or 'hihg' in text
    strikeIndex = 0
    if conditions:
        for word in words:
            strikeIndex += 1
            if word[0] == '$' and len(word) > 1:
                if word[1].isalpha():
                    for letter in word:
                        if letter.isalpha():
                            stock += letter
                            stock = stock.upper()
                    break
    strike = words[strikeIndex]
    if strike.upper().isupper():
        cp = strike[-1]
        strike = strike[0:-1] 
        if cp == 'p':
            call = False           
        elif cp == 'c':
            call = True
    if 'call' in text:
        call = True
    elif 'put' in text:
        call = False
    if 'next week' in text:
        year = '2022'
        month = '01'
        day = '07'
    else:
        year = '2021'
        month ='12'
        day = '21'
    expDate = year+'-'+ month+'-'+day
    f = open('blacklist.txt', 'w+')
    f.write(stock + '\n')
    if expDate and strike and stock and stock not in f.read():
        quantity, spread, bought, askPrice = buyOption(stock, expDate, strike, wb, psize, call)
        if bought:
            partialQuantity = quantity//3  
            remainder = quantity - partialQuantity * 2
            time.sleep(30)  
            sellOption(stock, expDate, strike, wb, partialQuantity)
            print("     manz Option: ", stock, "sell Time: ",
            time.ctime(time.time()), "Quantity: ", partialQuantity)        
            time.sleep(15)  
            sellOption(stock, expDate, strike, wb, partialQuantity)
            print("     manz Option: ", stock, "sell Time: ",
            time.ctime(time.time()), "Quantity: ", partialQuantity) 
            time.sleep(15)  
            sellOption(stock, expDate, strike, wb, remainder)
            print("     manz Option: ", stock, "sell Time: ",
            time.ctime(time.time()), "Quantity: ", remainder) 

