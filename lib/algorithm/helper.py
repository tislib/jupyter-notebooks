import pandas as pd


class PandasAlgorithmHelper:
    def __init__(self):
        self.df = pd.DataFrame(columns=['time', 'time_m', 'price', 'spread'])
        self.dfm = pd.DataFrame(columns=['time', 'time_m', 'price', 'spread'])

    def tick(self, time, price, spread):
        self.df = self.df.append(
            {
                'time': time,
                'time_m': time.replace(second=0, microsecond=0),
                'price': price,
                'spread': spread
            },
            ignore_index=True)
        # self.dfm =


class MavgHelper:

    def __init__(self, columns):
        self.mavg = {}
        self.items = []
        self.mavgMax = max(columns)
        self.columns = columns
        for col in self.columns:
            self.mavg[col] = None

    def push(self, price):
        self.items.append(price)

        if (len(self.items) > self.mavgMax):
            self.items = self.items[1:]

        for col in self.columns:
            if col <= len(self.items):
                s = sum(self.items[len(self.items) - col:])
                avg = s / col
                self.mavg[col] = round(avg * 10000000) / 10000000


class TickToHistorical:
    def __init__(self):
        self.items = []
        self.subscribers = []
        self.lastTime = None

    def tick(self, time, price, spread):
        time_m = time.replace(second=0, microsecond=0)
        if self.lastTime != time_m:
            for subs in self.subscribers:
                subs.reciveHistorical(time_m, price, spread)
        self.lastTime = time_m
