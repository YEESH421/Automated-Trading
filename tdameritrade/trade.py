from tda import auth, client
from tda.orders.common import Duration, Session, OptionInstruction, OrderType, OrderStrategyType
from tda.orders.generic import OrderBuilder
import tda
import json
import config
import datetime
import requests

#for some reason, we don't have access to tda.orders.options module, so here are the functions we need
def __base_builder():
    return (OrderBuilder()
            .set_session(Session.NORMAL)
            .set_duration(Duration.DAY))

def option_buy_to_open_market(symbol, quantity):
    '''
    Returns a pre-filled :class:`~tda.orders.generic.OrderBuilder` for a
    buy-to-open market order.
    '''
    return (__base_builder()
            .set_order_type(OrderType.MARKET)
            .set_order_strategy_type(OrderStrategyType.SINGLE)
            .add_option_leg(OptionInstruction.BUY_TO_OPEN, symbol, quantity))


def option_sell_to_close_market(symbol, quantity):
    '''
    Returns a pre-filled :class:`~tda.orders.generic.OrderBuilder` for a
    sell-to-close market order.
    '''
    from tda.orders.common import OptionInstruction, OrderType, OrderStrategyType

    return (__base_builder()
            .set_order_type(OrderType.MARKET)
            .set_order_strategy_type(OrderStrategyType.SINGLE)
            .add_option_leg(OptionInstruction.SELL_TO_CLOSE, symbol, quantity))

def equity_buy_market(symbol, quantity):
    '''
    Returns a pre-filled :class:`~tda.orders.generic.OrderBuilder` for an equity
    buy market order.
    '''
    from tda.orders.common import Duration, EquityInstruction
    from tda.orders.common import OrderStrategyType, OrderType, Session
    from tda.orders.generic import OrderBuilder

    return (OrderBuilder()
            .set_order_type(OrderType.MARKET)
            .set_session(Session.NORMAL)
            .set_duration(Duration.DAY)
            .set_order_strategy_type(OrderStrategyType.SINGLE)
            .add_equity_leg(EquityInstruction.BUY, symbol, quantity))

def equity_sell_market(symbol, quantity):
    '''
    Returns a pre-filled :class:`~tda.orders.generic.OrderBuilder` for an equity
    sell market order.
    '''
    from tda.orders.common import Duration, EquityInstruction
    from tda.orders.common import OrderStrategyType, OrderType, Session
    from tda.orders.generic import OrderBuilder

    return (OrderBuilder()
            .set_order_type(OrderType.MARKET)
            .set_session(Session.NORMAL)
            .set_duration(Duration.DAY)
            .set_order_strategy_type(OrderStrategyType.SINGLE)
            .add_equity_leg(EquityInstruction.SELL, symbol, quantity))

# authenticate
def authenticate():
    try:
        c = auth.client_from_token_file(config.token_path, config.tda_api_key)
    except FileNotFoundError:
        from selenium import webdriver
        wd = webdriver.Chrome(executable_path= config.chrome_driver_path)
        with wd as driver:
            c = auth.client_from_login_flow(
                driver, config.tda_api_key, config.redirect_uri, config.token_path)
    return c

def executeBuyOrderOption(symbol, quantity, c):
    builder = option_buy_to_open_market(symbol, quantity)
    order = builder.build()
    r = c.place_order(config.account_id, order)


def executeSellOrderOption(symbol, quantity, c):
    builder = option_sell_to_close_market(symbol, quantity)
    order = builder.build()
    r = c.place_order(config.account_id, order)

def executeBuyOrderEquity(symbol, quantity, c):
    builder = equity_buy_market(symbol, quantity)
    order = builder.build()
    r = c.place_order(config.account_id, order,)

def executeSellOrderEquity(symbol, quantity, c):
    builder = equity_sell_market(symbol, quantity)
    order = builder.build()
    r = c.place_order(config.account_id, order)

def getMarketCap(symbol):
    response = requests.get(
        "https://api.tdameritrade.com/v1/instruments", params={'apikey': config.tda_api_key, 'symbol': symbol, 'projection': 'fundamental'}
    )
    if symbol not in response.json():
        return -1
    else:
        return response.json()[symbol]['fundamental']['marketCap']
