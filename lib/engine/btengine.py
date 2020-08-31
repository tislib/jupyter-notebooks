from lib.engine.engine import Engine


class BackTestEngine(Engine):

    def init(self, sourceDf, algorithm, strategy):
        self.sourceDf = sourceDf
        self.algorithm = algorithm
        self.strategy = strategy
        self.tickCount = 0
        self.lastOrder = 0
        self.balance = 0
        self.lastOperation = 'closed'
        self.lastUnits = 0
        self.lostCount = 0
        self.wonCount = 0

    def run(self):
        for index, row in self.sourceDf.iterrows():
            self.runTick(row['time'], row['spread'], row['bid'], row['bid'])

    def runTick(self, time, spread, bid, ask):
        self.bid = bid
        self.ask = ask

        self.algorithm.tick(time, bid, spread)
        result = self.algorithm.signal()
        self.strategy.execute(time, result, self)
        self.tickCount = self.tickCount + 1
        if self.tickCount % 10000 == 0:
            print('tick processed ', time, self.tickCount, round(self.tickCount * 10000 / len(self.sourceDf)) / 100, '%', self.balance, self.wonCount + self.lostCount)

        if self.calculateEarning() >= 3 / 10000 and self.lastOrder != 0:
            print('fast closed')
            self.closeAllOrders()
        # if self.calculateEarning() < -3 / 10000 and self.lastOrder != 0:
        #     print('fast closed')
        #     self.closeAllOrders()

    def sell(self, units):
        self.closeAllOrders()

        self.lastUnits = units
        self.lastOperation = 'sell'
        self.lastOrder = self.bid

    def buy(self, units):
        self.closeAllOrders()

        self.lastUnits = units
        self.lastOperation = 'buy'
        self.lastOrder = self.ask

    def report(self):
        print('balance: ', self.balance)
        print('won count: ', self.wonCount)
        print('lost count: ', self.lostCount)


    def calculateEarning(self):
        earning = 0
        if self.lastOperation == 'sell':
            earning = self.lastOrder - self.bid
        if self.lastOperation == 'buy':
            earning = self.bid - self.lastOrder
        return earning

    def closeAllOrders(self):
        if self.lastOrder != 0:
            earning = self.calculateEarning()

            if earning > 0:
                self.wonCount = self.wonCount + 1
            #     print('earned: ', earning * self.lastUnits)
            #
            if earning < 0:
                self.lostCount = self.lostCount + 1
            #     print('lost: ', earning * self.lastUnits)

            self.balance = self.balance + earning * self.lastUnits
            self.lastOrder = 0