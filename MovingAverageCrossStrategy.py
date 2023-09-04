import backtrader as bt

class MovingAverageCrossStrategy(bt.Strategy):
    params = (
        ('fast', 20),
        ('slow', 50),
    )

    def __init__(self):
        self.order = None

        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast)
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()
        elif self.crossover < 0:
            self.order = self.sell()

    def notify_order(self, order):
        if order.status == order.Completed:
            dt = self.datas[0].datetime.datetime(0).isoformat()
            size = order.executed.size
            price = order.executed.price
            value = size * price
            cash = self.broker.get_cash()
            self.log('{} BUY {} at {} (value: {}, cash: {})'.format(
                dt, size, price, value, cash))

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        # dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))
        print(txt)
