'''

Computational Investing I - Georgia Tech
Home Work #3

@author: Ke-Wei Ma
@contact: keweima at gmail.com
@summary: Market Simulation Assignment

Portfolio returns analyzer
'''
import QSTK.qstkutil.tsutil as tsu
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

def print_performance( fund, bench):
    print "Details of the Performance of the portfolio :\n"

    print "Data Range : ", fund.index[0], " to " ,fund.index[-1],"\n"

    print "Sharpe Ratio of Fund : ", tsu.get_sharpe_ratio(tsu.daily(fund))[0]
    print "Sharpe Ratio of " + benchmark +" :", tsu.get_sharpe_ratio(tsu.daily(bench))[0],"\n"

    print 'Total Return of Fund :', (fund[-1] / fund[0] - 1) + 1
    print 'Total Return of ' + benchmark + ' : ', (bench[-1] / bench[0] -1) + 1, "\n"

    print 'Standard Deviation of Fund : ' + str(np.std(tsu.daily(fund.values)))
    print 'Standard Deviation of ' + benchmark + ' : ', np.std(tsu.daily(bench.values)), "\n"

    print 'Average Daily Return of Fund : ', np.mean( tsu.daily(fund.values))
    print 'Average Daily Return of ' + benchmark + ' : ', np.mean( tsu.daily(bench.values))


if __name__ == '__main__':

    fund_input_file = sys.argv[1]
    benchmark = sys.argv[2].strip().upper()

    fund = read_fund( fund_input_file)
    bench = read_benchmark( benchmark, list( fund.index))

    print_performance( fund, bench)
