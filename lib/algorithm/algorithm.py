class Algorithm:

    def tick(self, time, price, spread):
        raise Exception('UnsupportedOperationException')

    def signal(self):  # returns number between -1 and 1 , -1 is go down, 1 is go up, 0 is do nothing
        raise Exception('UnsupportedOperationException')

    pass
