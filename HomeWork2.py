'''

Computational Investing I - Georgia Tech
Home Work #2

@author: Ke-Wei Ma
@contact: keweima at gmail.com
@summary: Event Profiler Assignment
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import copy

def find_events(ls_symbols, d_data):

    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            price_today = df_close[s_sym].ix[ldt_timestamps[i]]
            price_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]

            # Event is defined as stock closing price crossing 5 bucks.
            if price_today < 5.0 and price_yest >= 5.0 :
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events



def doit(SPfname, pdfname) :

    dt_start = dt.datetime(2008, 1,1)
    dt_end = dt.datetime(2009, 12, 31)

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(SPfname)
    ls_symbols.append('SPY')

    # Obtain market data
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Clean market data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    print "Creating Event Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename=pdfname, b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')

if __name__ == '__main__':
    doit('sp5002008','HW2_EventStudy2008.pdf')
    doit('sp5002012','HW2_EventStudy2012.pdf')
