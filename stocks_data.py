import praw
import matplotlib.pyplot as plt
# import pandas_datareader as web
import pandas as pd
import datetime as dt
from yahoo_fin import stock_info as si

''' A tool to parse r/WSB for stock mentions in the Daily Discussion thread.'''

# to obfuscate the secret stuff
with open('secret_stuff.txt', 'r') as f:
    secret_list = []
    lines = f.readlines()
    for line in lines:
        secret_list.append(line.strip())
    client_id, client_secret, user_agent = secret_list

# note that username and password are not required if just gathering data (not posting, commenting, updooting, etc.)
username = ''
password = ''

# create the reddit object
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)


def stonk_counter(hot_subred):
    """count up the mentions of each stonk in the subreddit which is passed in as the hot_subred_object"""
    for post in hot_subred:
        # only parsing the Daily Discussion thread
        if 'Daily Discussion' in post.title:
            print(f'Post Title: {post.title}, upvotes: {post.ups}')
            # adjust limit arg (set low for testing)
            post.comments.replace_more(limit=10)
            mentions = 0
            list_of_stonks = read_stonk_tickers_from_file()
            mentions_dict = {}
            for stonk in list_of_stonks:
                mentions = 0
                for comment in post.comments.list():
                    if stonk in comment.body.split(' '):
                        mentions += 1
                    # get rid of stonks with very few mentions
                    if mentions > 30:
                        mentions_dict[stonk] = mentions
                    else:
                        pass
    print(f'Stonk Mentions: {mentions_dict}')
    return mentions_dict


def read_stonk_tickers_from_file():
    """read the list of the tickers available"""
    stonks_list = []
    with open('stonk_tickers.txt', 'r') as stonks_file:
        lines = stonks_file.readlines()
        for line in lines:
            stonks_list.append(line.strip())
        return stonks_list


def plot_results(vals, keys, pos):
    """plot the mentions of each ticker in a bar chart"""
    plt.bar(pos, vals, color='green')
    plt.xticks(ticks=pos, labels=keys)
    plt.xlabel('Stonk Ticker')
    plt.ylabel('Number of Mentions')
    plt.title('Mentions of Stock Tickers in Daily Discussion Thread\n'
              'on r/wallstreetbets')
    plt.show()


def stonks_to_buy(a_dict):
    """create the empty portfolio of the top 4 stocks from those mentioned"""
    portfolio = {}
    while (len(portfolio) < 4) and (len(a_dict) >= 1):
        keymax = max(a_dict, key=a_dict.get)
        del a_dict[keymax]
        portfolio[keymax] = 0
    return portfolio


def buy_stonks(portfolio, shares=10):
    """assumes 10 share purchase, fetches the price from the internet of each ticker
    and calculates the value of each position, puts it in the 'portolio' dictionary"""
    # downloads the current price on the date the script runs
    # takes principal, and splits evenly into each stock
    for key in portfolio.keys():
        price = si.get_live_price(key)
        value_each_ticker = shares * price
        portfolio[key] = value_each_ticker
    return portfolio


def get_portfolio_value(portfolio):
    """simple sum of all positions in portfolio and returns value"""
    total_value = 0
    for key in portfolio.keys():
        price = si.get_live_price(key)
        total_value += (portfolio[key])
    return total_value


# target the r/WSB sub
subred = reddit.subreddit('wallstreetbets')

# limit=None will provide all submissions (hard on the webservers, takes a long time)
hot_subred = subred.hot(limit=4)

try:
    # call our function to parse the post and rollup the mentions
    result_dict = stonk_counter(hot_subred)

    # call the plotter function to visualize the mentions
    # plot_results(result_dict.values(), result_dict.keys(), list(range(len(result_dict))))

    # create a new portfolio dictionary, which will track the value of our positions in each stonk
    portfolio = stonks_to_buy(result_dict)

    # accepts a dict, returns a dict with the value of each stonk in the portfolio, given X shares
    account_value = buy_stonks(portfolio)

except:
    print('An error occurred. This is likely because there is not a Daily Discussions post up in WSB.')

# returns a single dollar value of the portfolio
final_portfolio_value = get_portfolio_value(account_value)
performance_tracker_list = []
performance_tracker_list.append([final_portfolio_value, dt.datetime.today()])

# create a dataframe to dump into a .csv file for historical data on our portfolio's performance
performance_tracker_dataframe = pd.DataFrame(performance_tracker_list, columns=['Portfolio Value', 'Date'])

# add a column to calculate rolling performance of the portfolio
performance_tracker_dataframe['DoD % Change'] = 'NaN'

i = 1
print(portfolio)
for key in portfolio.keys():
    performance_tracker_dataframe[f'Position {i}'] = key
    print(key)
    i += 1

with open('stonksrollup.txt', 'r') as f:
    lines = f.readlines()
    if len(lines) == 0:
        # only write the header if it's the first time we're writing to the file
        performance_tracker_dataframe.to_csv('stonksrollup.txt', mode='a', index=None)
    else:
        performance_tracker_dataframe.to_csv('stonksrollup.txt', mode='a', index=None, header=None)

# TODO implement a second file which imports the functions in here and lets the user pick what they want to do
