'''

Computational Investing I - Georgia Tech
Home Work #3

@author: Ke-Wei Ma
@contact: keweima at gmail.com
@summary: Market Simulation Assignment

This implementation is based on the suggestions provided by instructor.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
#import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
#import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
#import datetime as dt
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import math
#import copy
import sys
import csv
import datetime as dt

# Read in orders file in CSV file format.  Return symbols and
# list of transaction dates
def read_orders( file_name) :

    symbols = set()     # uniqueness
    dates = []          # maintain sort order

    with open(file_name, 'rU') as csvfile:

        reader = csv.reader( csvfile, delimiter=',')
        for row in reader:

            s = row[3].strip().upper()  # Remove spaces, don't do it for numbers
                                        # because conversion does it auto-magically
            if s not in symbols:
                symbols.add( s)
            date = dt.datetime( int(row[0]), int(row[1]), int(row[2]))

            if date not in dates:
                dates.append(date)

    dates = sorted( dates)

    return symbols, dates

# From Yahoo finance, get close prices for 'symbols' for
# 'dates' given.
def read_market_data( symbols, dates):

    time_stamps = du.getNYSEdays( dates[0], dates[-1] + dt.timedelta(days=1), dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    close = dataobj.get_data( time_stamps, symbols, "close")
    close = close.fillna( method='ffill')
    close = close.fillna( method='bfill')

    return close, time_stamps

# Reread the order file but this time construct a table that
# indicates the number of shares held.  We now know the start and
# end date so we can pre-construct our matrices.
def compute_trade_matrix( file_name, symbols, time_stamps, price ):

    shares = np.zeros((len(time_stamps), len(symbols)))
    shares = pd.DataFrame( shares, index=time_stamps, columns=symbols)

    with open(file_name, 'rU') as csvfile:

        reader = csv.reader( csvfile, delimiter=',')
        for row in reader:

            # Extract relevant order information
            date = dt.datetime(int(row[0]), int(row[1]), int(row[2]),16)

            #print date
            ticker = row[3].strip().upper()
            order_type = row[4].strip().lower()
            quantity = int(row[5])

            # This will return index of multiple dates
            date_range = price.index[price.index == date]

            if order_type == "buy":
                shares.ix[date_range,ticker] += quantity
            elif order_type.lower() == "sell":
                shares.ix[date_range,ticker] -= quantity

    return shares

def compute_cash( initial_cash, trades, prices) :

    #print "\n\ntrades=", trades
    #print "\n\nprices=", prices

    # Multiply trades by prices to get cost per stock per day
    # Sum by date so we know the total equity value
    cost = -trades.mul( prices, axis=0).sum(axis=1)

    cost[0]+= initial_cash
    print "\n\ncost = ",cost

    # Now, shove this column back into share matrix
    trades['_CASH'] = cost
    trades = trades.cumsum()

    print "\n\nMatrix = ", trades

    return trades

def compute_fund_value( holdings, prices):

    # Add 1 to the prices so we can do matrix math easily
    #
    prices['_CASH'] = 1
    ts_fund = pd.TimeSeries(0.0, prices.index)

    for row_index, row in holdings.iterrows():
        print row.values.astype(float)
        print prices.ix[row_index].values
        ts_fund[row_index] += np.dot(row.values.astype(float), prices.ix[row_index].values)

    return ts_fund

if __name__ == '__main__':

    init_cash = float(sys.argv[1])
    orders_file_name = sys.argv[2]
    values_file_name = sys.argv[3]

    print "Initial cash =" , init_cash\

    symbols, dates = read_orders( orders_file_name)

    symbols = list(symbols)     # convert set to list

    print "symbols = ", symbols
    #print "dates = ", dates

    prices, dates = read_market_data(symbols, dates)

    print "close = ", prices
    print "dates = ", dates

    trade_matrix = compute_trade_matrix( orders_file_name, symbols, dates, prices)
    print "\n\nTrade Marix =\n", trade_matrix

    cash_matrix = compute_cash( init_cash, trade_matrix, prices)

    print "\n\ncash_matrix= \n", cash_matrix
    print "\n\nprice matrix= \n", prices


    fund = compute_fund_value( cash_matrix, prices)

    print "\n\nfund value = \n", fund