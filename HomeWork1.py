'''

Computational Investing 1
Home Work #1

Ke-Wei Ma
keweima@gmail.com

'''


# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Simulate one portfolio!
def simulate( na_rets, allocs) :

    # compute portfolio returns
    na_portrets = np.sum(na_rets * allocs, axis=1)

    cum_ret = na_portrets[-1]

    # compute daily returns, in-place
    tsu.returnize0(na_portrets)

    # compute statistics
    stddev_ret = np.std( na_portrets)
    daily_ret = np.mean( na_portrets)
    sharpe_ratio = np.sqrt(252) * daily_ret / stddev_ret

    return daily_ret, stddev_ret, cum_ret, sharpe_ratio

# Inelegant brute force search for global optimal portfolio
def optimize( na_rets) :

    best_sharpe = 0
    best_port = [0,0,0,0]

    for i in range( 0, 110, 10) :
        for j in range( 0, 110 - i, 10) :
            for k in range( 0, 110 - i - j, 10) :
                alloc = [i, j, k, 100 - i - j - k]
                alloc = [ x * 0.01 for x in alloc]

                x = simulate( na_rets, alloc)

                if x[3] > best_sharpe :
                    best_sharpe = x[3]
                    best_port = alloc

    return best_sharpe, best_port

def main():

    # Test case 1
    #syms = ['AAPL', 'GLD', 'GOOG', 'XOM']
    #dt_start = dt.datetime(2011,1,1)
    #dt_end = dt.datetime(2011,12,31)

    # Test case 2
    #syms = ['AXP', 'HPQ', 'IBM', 'HNZ']
    #dt_start = dt.datetime(2010,1,1)
    #dt_end = dt.datetime(2010,12,31)

    # Quiz - Question 1
    syms = ['C', 'GS', 'IBM', 'HNZ']
    dt_start = dt.datetime(2011,1,1)
    dt_end = dt.datetime(2011,12,31)

    # Quiz - Question 2
    syms = ['BRCM', 'TXN', 'AMD', 'ADI']
    dt_start = dt.datetime(2011,1,1)
    dt_end = dt.datetime(2011,12,31)

    # Creating an object of the dataaccess class with Yahoo as the source.
    #c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    c_dataobj = da.DataAccess('Yahoo')
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, syms, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Copying close price into separate dataframe to find rets
    df_rets = d_data['close'].copy()

    # Forward and back fill the data.
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')

    # Numpy matrix of filled data values
    na_rets = df_rets.values

    # Normalize price
    na_rets = na_rets / na_rets[0,:]

    sharpe, port = optimize(na_rets)
    print "Best Sharpe ratio is ", sharpe
    print "Portfolio = ", port

if __name__ == '__main__':
    main()
