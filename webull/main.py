from os import access
from webull import webull
import relogin

def buyOption(stock, expDate, strike, wb, psize, call):
    if call:
        t = 'call'
    elif not call:
        t = 'put'
    else:
        print('No call or put specified')
        return
    bought = False
    mktcap = float(wb.get_quote(stock)['marketValue'])
    option = wb.get_options_by_strike_and_expire_date(stock=stock, expireDate=expDate, strike=strike)
    print(option)
    id = option[0][t]['tickerId']
    askPrice = float(option[0][t]['askList'][0]['price'])
    quant = 0
    bidPrice = float(option[0][t]['bidList'][0]['price'])
    spread = askPrice - bidPrice
    contractPrice = askPrice * 100
    if contractPrice > 0:  # avoid division by 0
        quant = psize//contractPrice
    print(id, askPrice, quant)
    if askPrice > 0.05 and mktcap < 500000000000 and askPrice < 3:
        bought = True
        wb.place_order_option(optionId=id, lmtPrice= askPrice, action='BUY', orderType='LMT', quant=quant)
    return quant, spread, bought, askPrice

def sellOption(stock, expDate, strike, wb, quant):
    id = wb.get_options_by_strike_and_expire_date(stock=stock,expireDate=expDate, strike=strike)[0]['call']['tickerId']
    wb.place_order_option(optionId=id, action='SELL', orderType='MKT', quant=quant)

#tickerYYMMDDC12345678