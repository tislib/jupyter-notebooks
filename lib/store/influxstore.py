from influxdb import InfluxDBClient


class InfluxStore:
    def __init__(self):
        self.client = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', 'fbs')
        self.client.create_database('fbs')

    def store(self, item):
        self.client.write_points()

    def storeDf(self, df, key, version):
        cols = df.columns
        bulk = []
        i = 0
        for index, row in df.iterrows():
            time = row['time']
            row = row.drop('time')
            bulk.append({
                "measurement": "indicator",
                "tags": {
                    "key": key,
                    "version": version
                },
                "time": time,
                "fields": row.to_dict()
            })
            if len(bulk) > 1000:
                i = i + 1000
                rs = self.client.write_points(bulk)
                print(i)
                bulk = []

    def storeHDf(self, df):
        cols = df.columns
        i = 0
        bulk = []
        for index, row in df.iterrows():
            time = row['time']
            row = row.drop('time')
            bulk.append({
                "measurement": "historical",
                "time": time,
                "fields": row.to_dict()
            })
            if len(bulk) > 1000:
                i = i + 1000
                rs = self.client.write_points(bulk)
                print(i)
                bulk = []

    def prepareHS(self):
        self.client.query('select time, first(open) as open, max(max) as max, min(min) as min, last(close) as close into historical_weekly from historical group by time(1w)')
        self.client.query('select time, first(open) as open, max(max) as max, min(min) as min, last(close) as close into historical_hourly from historical group by time(1h)')
        self.client.query('select time, first(open) as open, max(max) as max, min(min) as min, last(close) as close into historical_daily from historical group by time(1d)')
