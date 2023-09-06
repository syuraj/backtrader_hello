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

        # above = bt.indicators.CrossOver(self.dataclose[0], self.currentATRTrailingStop)
        # below = bt.indicators.CrossDown(self.currentATRTrailingStop, self.dataclose[0])

        above = self.ema[0] > self.currentATRTrailingStop and self.dataclose[-1] < self.prevATRTrailingStop
        below = self.ema[0] < self.currentATRTrailingStop and self.dataclose[-1] > self.prevATRTrailingStop

        if self.dataclose[0] > self.currentATRTrailingStop and above:
            self.order = self.buy(size=1, exectype=bt.Order.StopTrail, trailpercent=self.params.longTrailPerc)
            print(f"Buy at {self.order.executed.size}")

        if self.dataclose[0] < self.currentATRTrailingStop and below:
            self.order = self.sell(size=1, exectype=bt.Order.StopTrail, trailpercent=self.params.shortTrailPerc)
            print(f"Sell at {self.order.executed.size}")

        self.prevATRTrailingStop = self.currentATRTrailingStop
        self.prevPos = self.currentPos
