import numpy as np
import pandas as pd


class AccuracyCalculator:
    @staticmethod
    def class_accuracy(cm):
        yesAcc = cm[0, 0] / (cm[0, 0] + cm[0, 1])
        noAcc = cm[1, 1] / (cm[1, 0] + cm[1, 1])
        accuracy = (yesAcc + noAcc) / 2

        print('class_accuracy => accuracy: ', accuracy, 'risk: ', AccuracyCalculator.class_accuracy_ret(cm))

    @staticmethod
    def class_accuracy_ret(cm):
        yesAcc = cm[0, 0] / (cm[0, 0] + cm[0, 1])
        noAcc = cm[1, 1] / (cm[1, 0] + cm[1, 1])

        risk = cm[0, 1] / (cm[0, 1] + cm[1, 1]) if (cm[0, 1] + cm[1, 1]) > 0 else 1

        return risk

    @staticmethod
    def optimistic_accuracy(y_pred, y_test, count):
        df = pd.DataFrame({'pred': y_pred, 'test': y_test})
        df = df.sort_values(by=['pred'], ascending=False)
        df = df.head(count)
        ok = len(df[df.test])
        all = len(df)
        risk = (all - ok) / all
        print('optimistic_accuracy => risk: ', risk, 'min pass point: ', df.iloc[count - 1, 0])

    @staticmethod
    def risk_hist(y_pred, y_test):
        df = pd.DataFrame({'pred': y_pred, 'test': y_test})
        df = df.sort_values(by=['pred'], ascending=False)
        df = df.round(2)
        df['ok'] = df['test'].astype(int)
        df['not_ok'] = 1 - df['test'].astype(int)
        df = df[['pred', 'ok', 'not_ok']].groupby('pred').agg('sum')
        df['risk'] = df['not_ok'] / (df['ok'] + df['not_ok'])
        df = df.sort_values(by=['pred'], ascending=False)
        return df


class Functions:
    @staticmethod
    def calc_integral(df):
        pass

    @staticmethod
    def calc_normal_dist(series, bound=1):
        max = series.max()
        min = series.min()

        def normalize(item):
            if item > 0:
                return item * (bound / max)
            else:
                return item * ((0 - bound) / min)
            pass

        return series.apply(normalize)

    @staticmethod
    def calc_equal_dist(series):
        def normalize(val):
            item = 2.71 ** val
            return item

        return series.apply(normalize)

    @staticmethod
    def seriesTrueCount(series):
        if (~series).all():
            return 0
        else:
            return series.value_counts()[True]
