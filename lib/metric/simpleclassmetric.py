from lib.helper import AccuracyCalculator, Functions
import numpy as np
import pandas as pd


class SimpleClassMetric:
    def __init__(self, df, sClass, sTruth, sValue):
        self.df = df[df.columns]
        self.sClass = sClass
        self.sTruth = sTruth
        self.sValue = sValue

    def calculate(self):
        self.calculateConfusionMatrix()
        self.calculateRiskIntervals()

        self.positiveMatch = self.tpCount / len(self.df)
        self.usage = self.tpCount / Functions.seriesTrueCount(self.sTruth)

        self.calculateValueMetrics()

    def calculateValueMetrics(self):
        self.wonValueSum = self.sValue[self.truePositive].sum()
        self.lostValueSum = abs(self.sValue[self.falsePositive].sum())

        self.resultValueSum = self.wonValueSum - self.lostValueSum
        
        self.wonValueCount = self.sValue[self.truePositive].count()
        self.lostValueCount = abs(self.sValue[self.falsePositive].count())

        self.resultValueCount = self.wonValueCount + self.lostValueCount

    def calculateConfusionMatrix(self):
        self.truePositive = self.sClass & self.sTruth
        self.falsePositive = self.sClass & ~self.sTruth

        self.trueNegative = ~self.sClass & ~self.sTruth
        self.falseNegative = ~self.sClass & self.sTruth

        self.tpCount = Functions.seriesTrueCount(self.truePositive)
        self.fpCpunt = Functions.seriesTrueCount(self.falsePositive)
        self.tnCount = Functions.seriesTrueCount(self.trueNegative)
        self.fnCount = Functions.seriesTrueCount(self.falseNegative)

        self.cm = np.array([[self.tnCount, self.fpCpunt], [self.fnCount, self.tpCount]])

        self.df['truePositive'] = self.truePositive
        self.df['falsePositive'] = self.falsePositive
        self.df['trueNegative'] = self.trueNegative
        self.df['falseNegative'] = self.falseNegative

        self.riskValue = AccuracyCalculator.class_accuracy_ret(self.cm)

    def show(self):
        print('___________RESULT___________')
        print('confusion matrix:', self.cm)
        AccuracyCalculator.class_accuracy(self.cm)
        print('class positive match:', self.positiveMatch)
        print('class positive match usage:', self.usage)
        print('________DAILY_METRICS_______')
        print('max daily risk', self.dailyRisk['risk'].max())
        print('daily risk plot:', self.dailyRisk['risk'].plot())
        print('________VALUE_METRICS_______')
        print('wonValueSum', self.wonValueSum)
        print('lostValueSum', self.lostValueSum)
        print('resultValueSum', self.resultValueSum)
        print('resultValueP', self.wonValueSum / (self.wonValueSum + self.lostValueSum))
        print('wonValueCount', self.wonValueCount)
        print('lostValueCount', self.lostValueCount)
        print('resultValueCount', self.resultValueCount)
        print('resultValueCountP', self.wonValueCount / (self.wonValueCount + self.lostValueCount))

    def calculateRiskIntervals(self):
        self.dailyRisk = self.df.groupby(pd.Grouper(key='time', freq='1d')).agg(
            {
                'truePositive': 'sum',
                'falsePositive': 'sum',
                'trueNegative': 'sum',
                'falseNegative': 'sum'
            }
        )
        self.dailyRisk['risk'] = self.dailyRisk['falsePositive'] / (
                    self.dailyRisk['falsePositive'] + self.dailyRisk['truePositive'])
        self.dailyRisk.dropna(inplace=True)
