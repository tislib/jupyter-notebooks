import pandas as pd
import numpy as np
import math
from datetime import datetime

from lib.files import histdata

coef1 = 10000


class DataSetOps:
    def __init__(self):
        self.df = pd.DataFrame()

    def import_data_set(self, histPath):
        df = pd.read_csv(histPath, sep=';')
        df.columns = ['date', 'open', 'max', 'min', 'close', '0']
        df['time'] = df['date'].map(self.parseTime)
        df.drop('0', axis=1, inplace=True)
        df['price'] = df['close']
        df['diff'] = df['price'].diff().shift(1)
        df['high'] = df['max']
        df['low'] = df['min']
        self.df = pd.concat([self.df, df])
        self.df.dropna(inplace=True)

    def prepareMin(self):
        self.df = self.df[['time', 'price']]
        self.df.dropna(inplace=True)

    def prepare10Min(self):
        self.df = self.df.groupby(pd.Grouper(key='time', freq='10min')).agg(
            {
                'open': 'first',
                'min': 'min',
                'max': 'max',
                'close': 'last'
            }
        )

        self.df['high'] = self.df['max']
        self.df['low'] = self.df['min']
        self.df['price'] = self.df['close']
        self.df['diff'] = self.df['price'].diff().shift(1)
        self.df['amp'] = self.df['max'] - self.df['min'].shift(-1)
        self.df['amp_n'] = self.df['min'] - self.df['max'].shift(-1)
        self.df['f_price'] = self.df['price'].shift(-1)
        self.df['f_min'] = self.df['min'].shift(-1)
        self.df['f_max'] = self.df['max'].shift(-1)
        self.df.dropna(inplace=True)
        self.df['time'] = self.df.index

    def import_tick_data_set(self, tickPath):
        df = pd.read_csv(tickPath, sep=',')
        df.columns = ['date', 'bid', 'ask', '0']
        df.drop('0', axis=1, inplace=True)
        df['time'] = df['date'].map(self.parseTime)
        df['price'] = df['bid']
        df['spread'] = round((df['ask'] - df['bid']) * 1000000) / 100
        df['diff'] = df['price'].diff().shift(1)
        self.df = pd.concat([self.df, df])

    def parseTime(self, dateStr):
        pattern = '%Y%m%d %H%M%S%f'
        return datetime.strptime(dateStr, pattern)

    def import_years(self, from_year, to_year):
        for year in range(from_year, to_year + 1):
            self.import_data_set(histdata['M1_' + str(year)])

    def prepare_past_values(self):
        for i in range(1, 64):
            self.df['val_past_' + str(i)] = self.df['value_d'].shift(i)

    def prepare(self):
        self.prepare_mavg(0, '')
        self.df = self.df.dropna()

    def prepareX(self):
        self.prepare_mavg(0, '')

    def prepare_mavg(self, shift, prefix):
        DataSetOps.prepare_mavg_static(self.df, shift, prefix)

    @staticmethod
    def prepare_mavg_static(df, shift, prefix):
        if prefix != '':
            prefix = prefix + '_'
            df[prefix + 'price'] = df['price'].shift(-shift)
        else:
            prefix = ''
        df[prefix + 'mavg10'] = (df[prefix + 'price'].rolling(window=10).mean())
        df[prefix + 'mavg20'] = (df[prefix + 'price'].rolling(window=20).mean())
        df[prefix + 'mavg30'] = (df[prefix + 'price'].rolling(window=30).mean())
        df[prefix + 'mavg40'] = (df[prefix + 'price'].rolling(window=40).mean())
        df[prefix + 'mavg50'] = (df[prefix + 'price'].rolling(window=50).mean())
        df[prefix + 'mavg60'] = (df[prefix + 'price'].rolling(window=60).mean())
        df[prefix + 'mavg70'] = (df[prefix + 'price'].rolling(window=70).mean())
        df[prefix + 'mavg80'] = (df[prefix + 'price'].rolling(window=80).mean())
        df[prefix + 'mavg90'] = (df[prefix + 'price'].rolling(window=90).mean())
        df[prefix + 'mavg100'] = (df[prefix + 'price'].rolling(window=100).mean())
        df[prefix + 'mavg1000'] = (df[prefix + 'price'].rolling(window=1000).mean())
        df[prefix + 'price_d'] = (df[prefix + 'price'] - df[prefix + 'price'].shift(1)) * coef1
        df[prefix + 'mavg10_d'] = (df[prefix + 'price'] - df[prefix + 'price'].rolling(window=10).mean()) * coef1
        df[prefix + 'mavg20_d'] = (df[prefix + 'price'] - df[prefix + 'price'].rolling(window=20).mean()) * coef1
        df[prefix + 'mavg100_d'] = (df[prefix + 'price'] - df[prefix + 'price'].rolling(window=100).mean()) * coef1
        df[prefix + 'mavg1000_d'] = (df[prefix + 'price'] - df[prefix + 'price'].rolling(window=1000).mean()) * coef1

    def prepare2(self, bound, window):
        self.df['has_down_v'] = (self.df['price'] - self.df['price'].shift(0 - window).rolling(
            window=window).min()) * coef1
        self.df['has_up_v'] = (self.df['price'].shift(-window).rolling(window=window).max() - self.df['price']) * coef1
        self.df['has_down'] = self.df['has_down_v'] > bound
        self.df['has_not_down'] = self.df['has_down_v'] < bound
        self.df['has_up'] = self.df['has_up_v'] > bound
        self.df['has_not_up'] = self.df['has_up_v'] < bound
        self.df['value_is_down'] = self.df['has_down'] & self.df['has_not_up']
        self.df['value_is_up'] = self.df['has_up'] & self.df['has_not_down']
