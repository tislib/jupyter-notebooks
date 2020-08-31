from lib.algorithm.algorithm import Algorithm
import random


class RandomAlgorithm(Algorithm):

    def tick(self, time, price, spread):
        print('tick', time, time.replace(second=0, microsecond=0), price, spread)
        pass

    def signal(self):  # returns number between -1 and 1 , -1 is go down, 1 is go up, 0 is do nothing
        return random.random() * 2 - 1