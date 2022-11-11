import datetime
from datetime import date
import yfinance as yf
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import datetime
from datetime import date
import yfinance as yf
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from os.path import exists
import os
import tensorflow.keras as keras
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import time


# import matplotlib.pyplot as plt


class Stocks:
    def __init__(self, symbol_lst, algorithm, forecast_time_span, max_depth=None, n_estimators=None, max_features=None,
                 seg_ratio=None, unit_a=None, unit_b=None, unit_c=None, epochs=None, batch_size=None):
        self.algorithm = algorithm
        self.data_points = 1000
        self.forecast_time_span = forecast_time_span
        self.delta_days = 720
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.seg_ratio = seg_ratio
        self.unit_a = unit_a
        self.unit_b = unit_b
        self.unit_c = unit_c
        self.epochs = epochs
        self.batch_size = batch_size
        self.symbol_lst = symbol_lst
        self.training_segment = None
        self.start = None
        self.end = None
        self.steps = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.steps = None
        self.model = None

        if algorithm in ['randomforest', 'lstm']:
            self.algorithm = algorithm
        else:
            raise ValueError(f'Machine learning algorithm: {algorithm} is not available.')

        if forecast_time_span in ['1d', '5d', '1mo']:
            self.forecast_time_span = forecast_time_span
        else:
            raise ValueError(f'Forecast time span of {forecast_time_span} is not available')

        # Steps are used for number of iterations to self feed back into the prediction/forecast model.
        # The granularity for these forecast time spans are something we will need to experiment with to achieve
        # the best prediction accuracy.
        if forecast_time_span == '1d':
            # About 7 hours in a trading day
            self.steps = 7
            self.granularity = '1h'
        if forecast_time_span == '5d':
            # About 35 hours in a 5-day trading period
            self.steps = 35
            self.granularity = '1h'
        if forecast_time_span == '1mo':
            # 21 days in a month
            self.steps = 21
            self.granularity = '1d'

        self.training_segment = self.seg_ratio * self.steps

    def get_mse(self):
        model = self.__train()
        prediction = self.__predict(model, self.x_test)
        mse = mean_squared_error(self.y_test, prediction)
        return mse

    def get_model(self):
        model = self.__train()
        return model

    def __train(self):
        model = None
        if self.algorithm == 'randomforest':
            model = self.__random_forest()
        if self.algorithm == 'lstm':
            model = self.__lstm()
        return model

    def __random_forest(self):
        x_train, y_train = self.__random_forest_training_data()
        model = RandomForestRegressor(max_depth=self.max_depth, random_state=123, n_estimators=self.n_estimators,
                                      max_features=self.max_features)
        model.fit(x_train, y_train)

        return model

    def __lstm(self):
        x_train, y_train = self.__lstm_training_data()
        model = keras.models.Sequential()
        model.add(LSTM(units=self.unit_a, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=self.unit_b, return_sequences=True))
        model.add(LSTM(units=self.unit_c))
        model.add(Dense(units=1))

        model.compile(loss="mse", optimizer='adam')
        # model.summary()
        model.fit(x_train, y_train, epochs=self.epochs, batch_size=self.batch_size, verbose=1, shuffle=False)
        return model

    def __predict(self, model, data):
        prediction = data
        x_predict = data

        for i in range(self.steps):
            if self.algorithm == 'lstm':
                scaler = MinMaxScaler(feature_range=(0, 1))
                x_predict = scaler.fit_transform(x_predict.reshape(-1, 1))
                x_predict = np.reshape(x_predict, (1, x_predict.shape[0], 1))
                next_predict = model.predict(x_predict)
                next_predict = scaler.inverse_transform(next_predict.reshape(-1, 1))
                prediction = np.append(prediction, next_predict)
                x_predict = prediction[-self.training_segment:].reshape(1, -1)
            else:
                next_predict = model.predict(x_predict)
                prediction = np.append(prediction, next_predict)
                x_predict = prediction[-self.training_segment:].reshape(1, -1)

        return prediction[-self.steps:]

    def __random_forest_training_data(self):
        delta = datetime.timedelta(days=self.delta_days)
        start_date = date.today() - delta
        end_date = date.today()
        x_train = []
        y_train = []
        for symbol in self.symbol_lst:
            data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                               interval=self.granularity)

            price_data = data.iloc[:]['Open'].values

            # Limit amount of data points. Too much data causes increased training time.
            if len(price_data) >= self.data_points:
                price_data = data.iloc[:]['Open'].values[-self.data_points:]
            else:
                price_data = data.iloc[:]['Open'].values[:]

            # Remove any NaN values from price_data
            index_lst = []
            for i in range(len(price_data)):
                if np.isnan(price_data[i]):
                    index_lst.append(i)
            price_data = np.delete(price_data, index_lst)

            # Method to create training data
            def create_dataset(dataframe):
                x = []
                y = []
                for i in range(self.training_segment, len(dataframe)):
                    x.append(dataframe[i - self.training_segment:i])
                    y.append(dataframe[i])
                return x, y

            x, y = create_dataset(price_data[0:-(self.training_segment + self.steps)])
            x_train = x_train + x
            y_train = y_train + y
            self.x_test = np.array(price_data[-(self.training_segment + self.steps): -self.steps]).reshape(1, -1)
            self.y_test = np.array(price_data[-self.steps:])
            time.sleep(2)
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        return x_train, y_train

    def __lstm_training_data(self):
        delta = datetime.timedelta(days=self.delta_days)
        start_date = date.today() - delta
        end_date = date.today()
        x_train = []
        y_train = []
        for symbol in self.symbol_lst:
            data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                               interval=self.granularity)
            data = data
            price_data = data.iloc[:]['Open'].values

            # Limit amount of data points. Too much data causes increased training time.
            if len(price_data) >= self.data_points:
                price_data = data.iloc[:]['Open'].values[-self.data_points:]
            else:
                price_data = data.iloc[:]['Open'].values[:]

            # Remove any NaN values from price_data
            index_lst = []
            for i in range(len(price_data)):
                if np.isnan(price_data[i]):
                    index_lst.append(i)
            price_data = np.delete(price_data, index_lst)

            # Method to create training
            def create_dataset(dataframe):
                dataframe = MinMaxScaler(feature_range=(0, 1)).fit_transform(dataframe.reshape(-1, 1))
                x = []
                y = []
                for i in range(self.training_segment, len(dataframe)):
                    x.append(dataframe[i - self.training_segment:i])
                    y.append(dataframe[i])
                return x, y

            x, y = create_dataset(price_data[0:-(self.training_segment + self.steps)])
            x_train = x_train + x
            y_train = y_train + y
            self.x_test = np.array(price_data[-(self.training_segment + self.steps): -self.steps]).reshape(1, -1)
            self.y_test = np.array(price_data[-self.steps:])

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        y_train = y_train.flatten()
        return x_train, y_train
