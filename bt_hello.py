# %% Import libraries
# from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import pandas as pd
import backtrader as bt
# from btplotting.analyzers import RecorderAnalyzer
from btplotting import BacktraderPlottingLive
# from btplotting.schemes import Blackly
# from btplotting.analyzers import RecorderAnalyzer
# from btplotting.feeds import FakeFeed

from btplotting import BacktraderPlotting
from btplotting.schemes import Tradimo

from MovingAverageCrossStrategy import MovingAverageCrossStrategy


# %matplotlib inline

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(MovingAverageCrossStrategy)
    cerebro.addanalyzer(BacktraderPlottingLive, address="*", port=8889)

    datapath = './datas/spx_2018_07.csv'
    df = pd.read_csv(datapath, index_col=0, parse_dates=True)

    data = bt.feeds.PandasData(dataname=df,
                        fromdate=datetime.datetime(2018, 7, 1),
                        todate=datetime.datetime(2018, 7, 2))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.Transactions)
    cerebro.addanalyzer(bt.analyzers.tradeanalyzer.TradeAnalyzer)

    cerebro.broker.setcash(100_000.0)

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
    plotter = BacktraderPlotting(style='bar', plot_mode='single', scheme=Tradimo())
    cerebro.plot(plotter, iplot=False)

