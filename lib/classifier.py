from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense

from sklearn.metrics import confusion_matrix
from lib.helper import AccuracyCalculator


class ComplexClassifier:
    def __init__(self):
        pass

    def addFeature(self):
        pass


# different tests for different features can result overfiting
class MavgComplexClassifier:
    def __init__(self, df, window=20, epilson=0.0001):
        self.df = df
        self.window = window
        self.epilson = epilson

        self.df['f_price'] = self.df['price'].shift(-window)
        self.df['value_real'] = self.df['f_price'] - self.df['price'] > self.epilson
        self.models = {}
        self.modelNames = []
        pass

    def add_feature(self, name, input_mavgv, output_mavg, batch_size=20, epochs=1):
        x_cols = ['price']
        for mavg in input_mavgv:
            x_cols.append('mavg' + str(mavg))
            self.df['mavg' + str(mavg)] = (self.df['price'].rolling(window=mavg).mean())
        self.df['mavg' + str(output_mavg)] = (self.df['price'].rolling(window=output_mavg).mean())
        self.df['f_mavg' + str(output_mavg)] = self.df['mavg' + str(output_mavg)].shift(-self.window)

        self.df['value_' + name] = self.df['f_mavg' + str(output_mavg)] - self.df[
            'mavg' + str(output_mavg)] > self.epilson

        self.df = self.df.dropna()
        X = self.df[x_cols]
        Y = self.df['value_' + name]

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        model = self.classify(X_train, y_train, len(x_cols), batch_size=batch_size, epochs=epochs)

        self.models[name] = model
        self.modelNames.append(name)

        self.show_result(model, X_test, y_test)

        self.df['predict_' + name] = model.predict(sc.transform(X))
        self.df['test_predict_' + name] = self.df['predict_' + name]

        return model

    def fix_min_feature_pass(self, min_pass_point=0.8):
        for f_name in self.modelNames:
            self.df[self.df['test_predict_' + f_name] < 0.8]['test_predict_' + f_name] = 0

    def train(self, batch_size=20, epochs=1):
        x_cols = []
        for f_name in self.modelNames:
            x_cols.append('predict_' + f_name)
        X = self.df[x_cols]
        Y = self.df['value_real']

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        model = self.classify(X_train, y_train, len(x_cols), batch_size=batch_size, epochs=epochs)

        self.show_result(model, X_test, y_test)

        self.df['result'] = model.predict(sc.transform(X))

    def classify(self, X_train, y_train, input_dim, batch_size=20, epochs=1):
        # Initializing Neural Network
        classifier = Sequential()

        class1 = Dense(output_dim=16, init='uniform', activation='relu', input_dim=input_dim)
        class2 = Dense(output_dim=16, init='uniform', activation='relu')
        # Adding the input layer and the first hidden layer
        classifier.add(class1)
        # Adding the second hidden layer
        classifier.add(class2)
        # Adding the output layer
        classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))

        # Compiling Neural Network
        from keras import metrics
        metric_names = [metrics.mae, 'accuracy']
        classifier.compile(optimizer='adam', loss='mean_squared_error', metrics=metric_names)

        # Fitting our model
        classifier.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)

        return classifier

    def show_result(self, classifier, X, y):
        # Creating the Confusion Matrix

        # Predicting the Test set results
        y_pred = classifier.predict(X)
        cm = confusion_matrix(y, (y_pred > 0.5))

        print(cm)

        AccuracyCalculator.class_accuracy(cm)
        AccuracyCalculator.optimistic_accuracy(y_pred[:, 0], y, 100)
        risk_hist_df = AccuracyCalculator.risk_hist(y_pred[:, 0], y)

        (1 - risk_hist_df.risk).plot()
