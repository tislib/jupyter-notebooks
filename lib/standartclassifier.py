class StandartClassifier:

    def init(self, X, y, batchSize, epocs):
        self.X = X
        self.Y = y
        self.batchSize = batchSize
        self.epochs = epocs
        self.initSets()

    def initSets(self):
        from sklearn.model_selection import train_test_split
        self.X_train, X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=0.1)
        self.X_test = X_test;

        from sklearn.preprocessing import StandardScaler
        self.sc = StandardScaler()
        self.X_train = self.sc.fit_transform(self.X_train)

    def initClassifier(self):
        # Importing the Keras libraries and packages

        # Initializing Neural Network
        import keras
        from keras.models import Sequential
        from keras.layers import Dense
        self.classifier = Sequential()

        class1 = Dense(output_dim=16, init='uniform', activation='relu', input_dim=len(self.X.columns))
        class2 = Dense(output_dim=16, init='uniform', activation='relu')
        class3 = Dense(output_dim=16, init='uniform', activation='relu')
        # Adding the input layer and the first hidden layer
        self.classifier.add(class1)
        # Adding the second hidden layer
        self.classifier.add(class2)
        self.classifier.add(class3)
        # Adding the output layer
        self.classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))

        # Compiling Neural Network
        from keras import metrics
        metric_names = [metrics.mae, 'accuracy']
        self.classifier.compile(optimizer='adam', loss='mean_squared_error', metrics=metric_names)

        # Fitting our model 
        self.classifier.fit(self.X_train, self.y_train, batch_size=self.batchSize, epochs=self.epochs)

    def saveModel(self):
        import random
        classfOutName = "/tmp/mavg_classifier_" + str(random.randint(100000, 999999));
        self.classifier.save(classfOutName)
        print('classifier saved to ', classfOutName)

    def run(self):
        self.runModel()

    def loadModel(self, path):
        import keras
        from keras.models import load_model
        self.classifier = load_model(path)

    def predictTest(self):
        self.y_pred = self.predict(self.X_test)

    def predict(self, X):
        # Predicting the Test set results
        return self.classifier.predict(self.sc.transform(X))

    def predictSingle(self, X):
        # Predicting the Test set results
        return self.classifier.predict(self.sc.transform([X]))[0][0]

    def runModel(self):
        self.initClassifier()

        self.saveModel()

        self.predictTest()
