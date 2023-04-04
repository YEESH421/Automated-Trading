import relogin
from main import *
from webull import webull
import sys

pin = ''
wb = webull()
relogin.relogin(wb)
wb.get_trade_token(pin)
psize = 2000 #position size

args = sys.argv[1]
i = 0
x = True
stock = ""
strike = ""
cp = ""
while x:
    char = args[i]
    if char.isalpha():
        stock += char
        i += 1
    else:
        x = False

x = True
while x:
    char = args[i]
    if char.isdigit() or char == '.':
        strike += char
        i += 1
    else:
        cp = char
        i += 1
        month = args[i:i+2]
        i += 2
        day = args[i:i+2]
        i += 2
        year = args[i:i+2]
        x = False

stock = stock.upper()
year = '20' + year
call = None
if cp == 'c':
    call = True
else:
    call = False
expDate = year + '-' + month + '-' + day
print("buying" + stock, strike, expDate)
buyOption(stock, expDate, strike, wb, psize, call)
print("bought" + stock, strike, expDate)