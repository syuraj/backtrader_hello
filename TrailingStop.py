from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import datetime
import pandas as pd
import backtrader as bt
from btplotting import BacktraderPlotting
from btplotting.schemes import Tradimo

class TrailingStop(bt.Strategy):
    params = dict(
        ma=bt.ind.SMA,
        p1=10,
        p2=30,
        stoptype=bt.Order.StopTrail,
        trailamount=100.0,
        trailpercent=0.0,
    )

    def __init__(self):
        # ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        # self.crup = bt.ind.CrossUp(ma1, ma2)
        self.order = None

    def next(self):
        print(f"self.position.size {self.position.size}")
        if not self.position.size:
            o = self.buy(exectype=self.p.stoptype,trailamount=self.p.trailamount)
            # self.order = None
            print('*' * 10)
        elif self.order is None:
            self.order = self.sell(exectype=self.p.stoptype,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent)

            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print(','.join(
                map(str, [self.datetime.date(), self.data.close[0],
                          self.order.created.price, tcheck])
                )
            )
            print('-' * 10)
        else:
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print(','.join(
                map(str, [self.datetime.date(), self.data.close[0],
                          self.order.created.price, tcheck])
                )
            )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                print('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                print('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


def runstrat():
    # args = parse_args(args)

    cerebro = bt.Cerebro()

    # Data feed kwargs
    datapath = './datas/NQ_test.csv'
    data0 = pd.read_csv(datapath, parse_dates=["Datetime"], index_col="Datetime")
    data = bt.feeds.PandasData(dataname=data0)
    cerebro.adddata(data)

    cerebro.addanalyzer(bt.analyzers.Transactions)

    # Broker
    # cerebro.broker = bt.brokers.BackBroker(**eval('dict(' + args.broker + ')'))
    cerebro.broker.setcash(50_000.0)

    # Sizer
    # cerebro.addsizer(bt.sizers.FixedSize, **eval('dict(' + args.sizer + ')'))

    # Strategy
    cerebro.addstrategy(TrailingStop)

    # Execute
    cerebro.run()

    plotter = BacktraderPlotting(style='bar', plot_mode='single', scheme=Tradimo())

    # cerebro.plot(plotter, iplot=False)

    cerebro.plot(plotter)


if __name__ == '__main__':
    runstrat()