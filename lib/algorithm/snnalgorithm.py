import random

from lib.algorithm.algorithm import Algorithm

from lib.algorithm.helper import PandasAlgorithmHelper, MavgHelper, TickToHistorical


class SimpleNeuralNetworkAlgorithm(Algorithm):
    def __init__(self, standartClassifier, columns):
        # self.df = self.df = pd.DataFrame(columns=['time', 'open', 'close', 'max', 'min'])
        self.pdHelper = PandasAlgorithmHelper()
        self.mavgHelper = MavgHelper([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000])
        self.tickToHistorical = TickToHistorical()
        self.tickToHistorical.subscribers.append(self)
        self.standartClassifier = standartClassifier
        self.columns = columns
        self.lastPrice = None
        self.mul = 10000

        self.maxv = 0
        self.minv = 1

    def tick(self, time, price, spread):
        price = price * self.mul
        # print('tick', time, time.replace(second=0, microsecond=0), price, spread)
        self.pdHelper.tick(time, price, spread)
        # self.dfh = self.pdHelper.df[['time_m', 'price', 'spread']].groupby('time_m').last()
        # DataSetOps.prepare_mavg_static(self.dfh, 0, '')
        self.tickToHistorical.tick(time, price, spread)
        self.lastPrice = price
        pass

    def reciveHistorical(self, time, price, spread):
        self.mavgHelper.push(price)
        # print('historical', len(self.mavgHelper.items))
        # print('historical', time, price, spread, self.mavgHelper.mavg[10])
        pass

    def signal(self):  # returns number between -1 and 1 , -1 is go down, 1 is go up, 0 is do nothing
        # val = ['price', 'mavg10', 'mavg20', 'mavg50', 'mavg80', 'mavg100', 'mavg1000']
        val = [
            self.lastPrice,
            self.mavgHelper.mavg[10],
            self.mavgHelper.mavg[20],
            self.mavgHelper.mavg[50],
            self.mavgHelper.mavg[80],
            self.mavgHelper.mavg[100]
        ]
        if self.mavgHelper.mavg[100] is not None:
            return self.standartClassifier.predictSingle(val)
        return 0

    def prepareHistorical(self):
        self.pdHelper.df['time_m'] = self.pdHelper.df['time'].map(lambda time: time.replace(second=0, microsecond=0))
