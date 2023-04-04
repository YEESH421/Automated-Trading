from manzparse import parseAndBuyManzAlert
from mmaparse import * 
from joetweetparse import *
from webull import webull 
from relogin import *
import time
#tweet = '$CALX - $105 CALLS EXP. 1/21/22 @ $0.35-$0.40'
tweet = '🌙FIRE DAY-TRADE / POSSIBLE SCALP🌙 \n$FUBO - $15 CALLS EXP. 1/14 @ $0.27-$0.28'
wb = webull()
relogin(wb)
#wb.get_account_id()
wb.get_trade_token('')

#time.sleep(600)
#tweet = '$AMD Dec 31th $160 calls, small entry for a swing'
#print(wb.get_options_by_strike_and_expire_date('AMD','2022-02-11', '160'))
print(buyOption('AMD','2022-02-11', '160' ,wb, 200, 't'))
#parseAndBuyMMAAlert(tweet, 30, 0, wb)
#parseAndBuyJoeAlert(tweet, 0, 0, wb)
#parseAndBuyManzAlert(tweet, 30, 0, wb)
#print(wb.get_quote('AAPL'))
#print('12345'[:-1])

#sellOption('CRTX', '2022-01-21', '17.5', wb, )