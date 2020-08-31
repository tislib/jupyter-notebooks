import random

from lib.algorithm.algorithm import Algorithm

from lib.algorithm.helper import PandasAlgorithmHelper, MavgHelper, TickToHistorical
import pandas as pd


class Amp1Algorithm(Algorithm):
    def __init__(self, winMin, winMax):
        self.winMin = winMin
        self.winMax = winMax

        self.lastPrice = 0
        self.lastMax = 0
        self.lastMin = 2
        self.lastTime = 0

        self.curPrice = 0
        self.curMax = 0
        self.curMin = 2
        self.lastTimeC = None

        self.lastSignal = 0
        self.lastAmp = 0
        self.data = pd.DataFrame()

    def tick(self, time, price, spread):
        if self.lastTime == 0:
            self.prepareInitial(price)

        time_m = time.replace(second=0, microsecond=0)

        time_m = time_m.to_datetime64().astype(int) / (1000 * 1000 * 1000 * 60)

        m_minute = time_m % 10

        if m_minute == 0 and self.lastTime != time_m:
            amp = self.lastMax - self.curMin
            # print(amp * 10000, (amp * 10000 > self.winMin), (amp * 10000 < self.winMax))
            if (amp * 10000 > self.winMin) & (amp * 10000 < self.winMax):  # & (spread < 0.3):
                self.lastSignal = -1
                print(time, 'signalled')
            else:
                self.lastSignal = 'close-all'

            if self.lastTimeC:
                self.data = self.data.append({
                    'time': self.lastTimeC,
                    'min': self.lastMin,
                    'max': self.lastMax,
                    'close': self.lastPrice,
                    'amp': self.lastAmp,
                }, ignore_index=True)

            self.lastTime = time_m
            self.lastTimeC = time.replace(second=0, microsecond=0)
            self.lastPrice = price
            self.lastMax = self.curMax
            self.lastMin = self.curMin
            self.curMax = 0
            self.curMin = 2
            self.lastAmp = amp

        else:
            self.lastSignal = 0

        if self.curMax < price:
            self.curMax = price

        if self.curMin > price:
            self.curMin = price

    def signal(self):
        return self.lastSignal

    def prepareInitial(self, price):
        self.lastPrice = price
        self.lastMax = price
        self.lastMin = price
