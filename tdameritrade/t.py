import trade
import sys

def format(stock, strike, date, cp):
    d = date.split('/')
    month = d[0]
    day = d[1]
    return stock + '_' + month + day + '21' + cp + strike

def determineQuantityO(m, c, symbol):
    quantity = -1
    quote = c.get_quote(symbol).json()
    contractPrice = quote[symbol]['askPrice'] * 100
    if contractPrice > 0:  # avoid division by 0
        quantity = int(m//contractPrice)
    return quantity

c = trade.authenticate()
argList = sys.argv[1:]
cName = format(argList[0], argList[1], argList[2], argList[3])
print(cName)
quantity = determineQuantityO(500, c, cName)
trade.executeBuyOrderOption(cName, quantity, c)