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
import yfinance as yf
from btplotting import BacktraderPlotting
from btplotting.schemes import Tradimo
import os
# from MovingAverageCrossStrategy import MovingAverageCrossStrategy
from BreadBankStrategy2 import BreadBankStrategy2
# from TrailingStop import TrailingStop
# import pytz
# from RandomStrat import RandomStrat
# %matplotlib inline

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(BreadBankStrategy2)
    # cerebro.addanalyzer(BacktraderPlottingLive, address="*", port=8889)

    # datapath = './datas/spx_2018_07.csv'
    # df = pd.read_csv(datapath, index_col=0, parse_dates=True)

    # data = bt.feeds.PandasData(dataname=df,
    #                     fromdate=datetime.datetime(2018, 7, 1),
    #                     todate=datetime.datetime(2018, 7, 20),
    #                     timeframe=bt.TimeFrame.Minutes,
    #                     compression=1)

    datapath = './datas/NQ1.csv'
    if os.path.exists(datapath):
        data = pd.read_csv(datapath, parse_dates=["Datetime"], index_col="Datetime")
    else:
        data = yf.download('NQ=F', start='2023-09-01', end='2023-09-07', interval='1m', auto_adjust=True)
        # desired_timezone = pytz.timezone('America/New_York')
        # data.index = data.index.tz_convert(desired_timezone)
        data.to_csv(datapath)

    data = bt.feeds.PandasData(dataname=data)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.Transactions)
    cerebro.addanalyzer(bt.analyzers.tradeanalyzer.TradeAnalyzer)

    cerebro.broker.setcash(50_000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)

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

    # cerebro.plot()
    # cerebro.plot(plotter)
    cerebro.plot(plotter, iplot=False)

