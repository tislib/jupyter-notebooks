class SimpleStrategy:

    def __init__(self):
        self.upc = 0
        self.isUp = False

    def execute(self, time, signal, engine):  # prediction is between -1 to 1
        if signal == 'close-all':
            engine.closeAllOrders()
        elif signal > 0.5:
            engine.buy(1000)

        elif signal < -0.5:
            engine.sell(1000)
