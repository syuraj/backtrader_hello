import backtrader as bt

class BreadBankStrategy2(bt.Strategy):
    params = (
        ('longProfitPerc', 0.023),
        ('shortProfitPerc', 0.02),
        ('longTrailPerc', 0.003),
        ('shortTrailPerc', 0.001),
        ('sensitivity', 14),
        ('atrPeriod', 11),
        ('heikenSignal', True)
    )

    def __init__(self):
        self.order = None
        self.trailing_stop = None
        self.prevATRTrailingStop = 0.0
        self.currentATRTrailingStop = 0.0
        self.prevPos = 0
        self.currentPos = 0
        self.atr = bt.indicators.AverageTrueRange(period=self.params.atrPeriod)
        self.ema = bt.indicators.ExponentialMovingAverage(period=1)

        self.dataclose = self.datas[0].close

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if len(self.dataclose) < self.params.atrPeriod:
            return

        if not self.position.size:
            xATR = self.atr
            nLoss = self.params.sensitivity * xATR

            # if self.params.heikenSignal:
            #     src = bt.heikinashi(self.data)

            iff_1 = self.dataclose[0] -  nLoss if self.dataclose[0] > self.prevATRTrailingStop else self.dataclose[0] +  nLoss
            iff_2 = min(self.prevATRTrailingStop, self.dataclose[0] + nLoss) if self.dataclose[0] < self.prevATRTrailingStop and self.dataclose[-1] < self.prevATRTrailingStop else iff_1
            self.currentATRTrailingStop = max(self.prevATRTrailingStop, self.dataclose[0] - nLoss) if self.dataclose[0] > self.prevATRTrailingStop and self.dataclose[-1] > self.prevATRTrailingStop else iff_2

            self.currentPos = 0
            iff_3 = -1  if self.dataclose[-1] > self.prevATRTrailingStop and self.dataclose[0] < self.prevATRTrailingStop else self.prevPos
            self.currentPos = 1 if self.dataclose[-1] < self.prevATRTrailingStop and self.dataclose[0] > self.prevATRTrailingStop else iff_3

            # print(f"iff_1: {iff_1}")
            # print(f"iff_2: {iff_2}")
            # print(f"iff_3: {iff_3}")

            above = self.ema[0] > self.currentATRTrailingStop and self.dataclose[-1] < self.prevATRTrailingStop
            below = self.ema[0] < self.currentATRTrailingStop and self.dataclose[-1] > self.prevATRTrailingStop

            if self.dataclose[0] > self.currentATRTrailingStop and above:
                self.order = self.buy(size=1)
                print(f"Buy at {self.order.executed.size}")

            if self.dataclose[0] < self.currentATRTrailingStop and below:
                self.order = self.sell(size=1)
                print(f"Sell at {self.order.executed.size}")

            self.prevATRTrailingStop = self.currentATRTrailingStop
            self.prevPos = self.currentPos

        else:
            if not self.trailing_stop:
                # trail_percent = self.params.trailpercent
                # current_price = self.data.close[0]
                # trailing_stop_price = current_price - (current_price * trail_percent)

                # Create a trailing stop order for the current position
                if self.position.size > 0:
                    self.trailing_stop = self.sell(
                        exectype=bt.Order.StopTrail,
                        trailpercent=self.params.shortTrailPerc,
                        # price=trailing_stop_price,
                    )
                elif self.position.size < 0:
                    self.trailing_stop = self.buy(
                        exectype=bt.Order.StopTrail,
                        trailpercent=self.params.longTrailPerc,
                        # price=trailing_stop_price,
                    )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                print('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                print('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f'order.Margin: {order.Margin}')

        self.order = None  # no pending order
        self.trailing_stop = None
