
from lib.files import histdata
from lib.dataset import DataSetOps

dataSetOps = DataSetOps()

dataSetOps.import_data_set(histdata['M1_2016'])
print(len(dataSetOps.df))
dataSetOps.import_data_set(histdata['M1_2017'])

dataSetOps.prepare2()

df = dataSetOps.df

print(df.head())

print(len(df))