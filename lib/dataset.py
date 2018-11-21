import pandas as pd
import numpy as np
import math
from lib.files import histdata

coef1 = 10000


class DataSetOps:
    def __init__(self):
        self.df = pd.DataFrame()

    def import_data_set(self, histPath):
        df = pd.read_csv(histPath, sep=';')
        df.columns = ['date', 'open', 'max', 'min', 'close', '0']
        df.drop('0', axis=1, inplace=True)
        df['price'] = df['close']
        df['diff'] = df['price'].diff().shift(1)
        self.df = pd.concat([self.df, df])

    def import_years(self, from_year, to_year):
        for year in range(from_year, to_year + 1):
            self.import_data_set(histdata['M1_' + str(year)])
            
    def prepare_past_values(self):
        for i in range(1, 64):
            self.df['val_past_' + str(i)] = self.df['value_d'].shift(i)

    def prepare(self):
        self.prepare_mavg(0, '')

    def prepare_mavg(self, shift, prefix):
        if prefix != '':
            prefix = prefix + '_'
            self.df[prefix + 'price'] = self.df['price'].shift(-shift)
        else: 
            prefix = ''
        self.df[prefix + 'mavg10'] = (self.df[prefix + 'price'].rolling(window=10).mean())
        self.df[prefix + 'mavg20'] = (self.df[prefix + 'price'].rolling(window=20).mean())
        self.df[prefix + 'mavg30'] = (self.df[prefix + 'price'].rolling(window=30).mean())
        self.df[prefix + 'mavg40'] = (self.df[prefix + 'price'].rolling(window=40).mean())
        self.df[prefix + 'mavg50'] = (self.df[prefix + 'price'].rolling(window=50).mean())
        self.df[prefix + 'mavg60'] = (self.df[prefix + 'price'].rolling(window=60).mean())
        self.df[prefix + 'mavg70'] = (self.df[prefix + 'price'].rolling(window=70).mean())
        self.df[prefix + 'mavg80'] = (self.df[prefix + 'price'].rolling(window=80).mean())
        self.df[prefix + 'mavg90'] = (self.df[prefix + 'price'].rolling(window=90).mean())
        self.df[prefix + 'mavg100'] = (self.df[prefix + 'price'].rolling(window=100).mean())
        self.df[prefix + 'mavg1000'] = (self.df[prefix + 'price'].rolling(window=1000).mean())
        self.df[prefix + 'price_d'] = (self.df[prefix + 'price'] - self.df[prefix + 'price'].shift(1)) * coef1
        self.df[prefix + 'mavg10_d'] = (self.df[prefix + 'price'] - self.df[prefix + 'price'].rolling(window=10).mean()) * coef1
        self.df[prefix + 'mavg20_d'] = (self.df[prefix + 'price'] - self.df[prefix + 'price'].rolling(window=20).mean()) * coef1
        self.df[prefix + 'mavg100_d'] = (self.df[prefix + 'price'] - self.df[prefix + 'price'].rolling(window=100).mean()) * coef1
        self.df[prefix + 'mavg1000_d'] = (self.df[prefix + 'price'] - self.df[prefix + 'price'].rolling(window=1000).mean()) * coef1

        self.df = self.df.dropna()
        
    def prepare2(self, bound, window):
        self.df['has_down_v'] = (self.df['price'] - self.df['price'].shift(0-window).rolling(window=window).min()) * coef1
        self.df['has_up_v'] = (self.df['price'].shift(-window).rolling(window=window).max() - self.df['price']) * coef1
        self.df['has_down'] = self.df['has_down_v'] > bound
        self.df['has_not_down'] = self.df['has_down_v'] < bound
        self.df['has_up'] = self.df['has_up_v'] > bound
        self.df['has_not_up'] = self.df['has_up_v'] < bound
        self.df['value_is_down'] = self.df['has_down'] & self.df['has_not_up']
        self.df['value_is_up'] = self.df['has_up'] & self.df['has_not_down']
