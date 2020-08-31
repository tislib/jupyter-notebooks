class TakeAlgorithm:

    @staticmethod
    def pdTake(algoName, action='sell', **kwargs):
        if algoName == 'simple':
            return lambda row: TakeAlgorithm.simpleTake(
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                action,
                kwargs['spread'],
                kwargs['stopLose'],
                kwargs['takeProfit']
            )

    @staticmethod
    def simpleTake(o, h, l, c, action, spread, stopLose, takeProfit):
        if action == 'buy':
            stopLosePrice = (o - l) + (spread / 10000)
            takeProfitPrice = (h - o) - (spread / 10000)
            if stopLosePrice > (stopLose / 10000):
                return 0 - stopLosePrice

            if takeProfitPrice > (takeProfit / 10000):
                return takeProfitPrice

            return c - o - (spread / 10000)

        if action == 'sell':
            stopLosePrice = (h - o) + (spread / 10000)
            takeProfitPrice = (o - l) - (spread / 10000)
            if stopLosePrice > (stopLose / 10000):
                return 0 - stopLosePrice

            if takeProfitPrice > (takeProfit / 10000):
                return takeProfitPrice

            return o - c - (spread / 10000)

    @staticmethod
    def metrics(df, algoName, inplace=False, **kwargs):
        simple_sell_value_algo = TakeAlgorithm.pdTake(algoName, action='sell', **kwargs)
        simple_buy_value_algo = TakeAlgorithm.pdTake(algoName, action='buy', **kwargs)

        simple_sell_value = df.apply(simple_sell_value_algo, axis=1)
        simple_buy_value = df.apply(simple_buy_value_algo, axis=1)

        ssvp = simple_sell_value > 0
        sbvp = simple_buy_value > 0
        bothvp = ssvp & sbvp
        nonevp = ~ssvp & ~sbvp

        print('count df', len(df))
        print('count simple_sell_value', len(df[simple_sell_value > 0]))
        print('count simple_buy_value', len(df[simple_buy_value > 0]))
        print('count both', len(df[bothvp]))
        print('count none', len(df[nonevp]))

        print('sum simple_sell_value', simple_sell_value.sum())
        print('sum simple_buy_value', simple_buy_value.sum())

        if ~inplace:
            df['simple_sell_value'] = simple_sell_value
            df['simple_buy_value'] = simple_buy_value

    @staticmethod
    def pdCalc(df, algoName, inplace=False, **kwargs):
        simple_sell_value_algo = TakeAlgorithm.pdTake(algoName, action='sell', **kwargs)
        simple_buy_value_algo = TakeAlgorithm.pdTake(algoName, action='buy', **kwargs)

        simple_sell_value = df.apply(simple_sell_value_algo, axis=1)
        simple_buy_value = df.apply(simple_buy_value_algo, axis=1)

        if ~inplace:
            df['simple_sell_value'] = simple_sell_value
            df['simple_buy_value'] = simple_buy_value
        else:
            df2 = df[df.columns]
            df2['simple_sell_value'] = simple_sell_value
            df2['simple_buy_value'] = simple_buy_value
            return df2
