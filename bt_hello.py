# %% Import libraries
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import backtrader as bt
from TestStrategy import TestStrategy
import pandas as pd

# %matplotlib inline

class CustomCSVData(bt.feeds.GenericCSVData):
    params2 = (
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', 6),
    )

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    datapath = './datas/spx_2018_07.csv'
    df = pd.read_csv(datapath, index_col=0, parse_dates=True)

    data = bt.feeds.PandasData(dataname=df,
                        fromdate=datetime.datetime(2018, 7, 1),
                        todate=datetime.datetime(2018, 7, 5))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.broker.setcommission(commission=0.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    start = datetime.datetime.now()
    cerebro.run()
    stop = datetime.datetime.now()

    print(f"Time taken: {(stop-start).total_seconds()} seconds")
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
