import string
import random

class FeatureDetectVisualite:
	def __init__(self, df, feature_detect_column):
		self.df = df
		self.feature_detect_column = feature_detect_column

		self.window = 64

	def prepare(self):
		for i in range(1, self.window):
 	   		self.df['val_past_' + str(i)] = self.df['price'].shift(i)
			self.df['mavg10_past_' + str(i)] = self.df['mavg10'].shift(i)
			self.df['mavg100_past_' + str(i)] = self.df['mavg100'].shift(i)
			self.df['mavg1000_past_' + str(i)] = self.df['mavg1000'].shift(i)
		self.df2 = self.df[self.df[self.feature_detect_column]]
		self.df2.reset_index(drop=True, inplace=True)
		return self.df2

	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(int(size)))

	def prepare_sub(self, index):
		res = []
		for i in range(1, self.window):
			res.append(self.df2['val_past_' + str(i)].get(index))
		return res

	def make(self):
		output = '/var/www/html/' + self.id_generator()
		return output
