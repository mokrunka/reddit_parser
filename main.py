import praw
import matplotlib.pyplot as plt
# import pandas_datareader as web
import pandas as pd
import datetime as dt
from yahoo_fin import stock_info as si
from stocks_data import stonk_counter
from stocks_data import read_stonk_tickers_from_file
from stocks_data import plot_results
from stocks_data import stonks_to_buy
from stocks_data import buy_stonks
from stocks_data import get_portfolio_value

# ''' A tool to parse r/WSB for stock mentions in the Daily Discussion thread.'''
#
# client_id = '6GW5cwGKXZODxw'
# client_secret = 'RmVV6kbWvgHjXO8eI4I2USBUTCK6JA'
# user_agent = 'stocks_data'
# # note that username and password are not required if just gathering data (not posting, commenting, updooting, etc.)
# username = ''
# password = ''
#
# # create the reddit object
# reddit = praw.Reddit(client_id=client_id,
#                      client_secret=client_secret,
#                      user_agent=user_agent,
#                      username=username,
#                      password=password)
def initialize():
    """this function will present a menu with options for the user"""
    ''' A tool to parse r/WSB for stock mentions in the Daily Discussion thread.'''

    somedict = stonk_counter(hot_subred)
    portfolio = stonks_to_buy(somedict)
    running = True
    while running:
        print(f'Menu:\n'
              f'1: plot_results\n'
              f'2: stonks_to_buy (print them)\n'
              f'3: buy_stonks\n'
              f'4: Quit\n')
        choice = int(input('Enter a selection: '))
        if choice == 1:
            print(somedict.values(), somedict.keys(), list(range(len(somedict))))
            plot_results(somedict.values(), somedict.keys(), list(range(len(somedict))))
        elif choice == 2:
            print(portfolio)
        elif choice == 3:
            principal = int(input('How much money would you like to invest? '))
            account_value = buy_stonks(portfolio, principal)
        elif choice == 4:
            running = False


if __name__ == '__main__':
    initialize()
