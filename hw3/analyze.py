'''

Computational Investing I - Georgia Tech
Home Work #3

@author: Ke-Wei Ma
@contact: keweima at gmail.com
@summary: Market Simulation Assignment

Portfolio returns analyzer
'''

import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import pandas as pd
import numpy as np
import sys
import csv
import datetime as dt

def read_fund( file_name) :

    prices = []
    dates = []

    with open(file_name, 'rU') as csvfile:

        reader = csv.reader( csvfile, delimiter=',')

        for row in reader:

            dates.append( dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16))
            prices.append(float(row[3]))


    fund = pd.TimeSeries( dict( zip(dates, prices)))
    return fund


# Retrieve historical prices for the benchmark
def read_benchmark( symbol, time_stamps):

    dataobj = da.DataAccess('Yahoo')
    close = dataobj.get_data( time_stamps, [symbol], "close")
    close = close.fillna( method='ffill')
    close = close.fillna( method='bfill')

    return close[symbol]


if __name__ == '__main__':

    fund_input_file = sys.argv[1]
    benchmark = sys.argv[2].strip().upper()

    #print fund_input_file, ",", benchmark

    fund = read_fund( fund_input_file)
    benchmark_prices = read_benchmark( benchmark, list( fund.index))

    print "fund = ", fund
    print "bench = ", benchmark_prices