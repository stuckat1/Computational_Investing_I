'''

Computational Investing I - Georgia Tech
Home Work #3

@author: Ke-Wei Ma
@contact: keweima at gmail.com
@summary: Market Simulation Assignment
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
def compute_trades( file_name, symbols, time_stamps, price ):

    shares = np.zeros((len(time_stamps), len(symbols)))
    shares = pd.DataFrame( shares, index=time_stamps, columns=symbols)
    print "********************"
    print shares
    print "********************"


    print "Compute_trades"
    with open(file_name, 'rU') as csvfile:

        reader = csv.reader( csvfile, delimiter=',')
        for row in reader:

            #print shares
            #print price

            # reconstruct date from file
            date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
            #print price.index
            #print date
            ticker = row[3].strip().upper()
            order_type = row[4].strip().lower()
            quantity = int(row[5])
            # get range of dates

            print "^^^^^"
            date_range = price.index[price.index >= date]
            print date_range
            print shares.ix[date_range]
            print "^^^^^"
            #print "***", ticker, order_type, quantity, date
            #print ">>>", date_range
            #print "<<<"
            print "*",order_type,"*"
            if order_type == "buy":
                #shares.ix[date_range][ticker] += float(quantity)
                shares.ix[date_range,ticker] += quantity
            elif order_type.lower() == "sell":
                shares.ix[date_range,ticker] -= quantity

    return shares

if __name__ == '__main__':

    init_cash = sys.argv[1]
    orders_file_name = sys.argv[2]
    values_file_name = sys.argv[3]

    print init_cash, ", ", orders_file_name ,",", values_file_name

    symbols, dates = read_orders( orders_file_name)

    print "symbols = ", symbols
    print "dates = ", dates

    prices, dates = read_market_data( list(symbols), dates)

    print "close = ", prices
    print "dates = ", dates

    x = compute_trades( orders_file_name, symbols, dates, prices)
    print x