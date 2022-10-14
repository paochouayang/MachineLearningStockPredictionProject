import datetime
from datetime import date
import yfinance as yf
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# import matplotlib.pyplot as plt


class Stocks:
    def __init__(self, symbol, algorithm, forecast_time_span, max_depth, n_estimators, max_features, seg_ratio):
        self.symbol = symbol
        self.algorithm = algorithm
        self.data_points = 1000
        self.forecast_time_span = forecast_time_span
        self.delta_days = 720
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.seg_ratio = seg_ratio
        self.training_segment = None
        self.start = None
        self.end = None
        self.steps = None
        self.data = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.steps = None

        if algorithm in ['randomforest', 'lstm']:
            self.algorithm = algorithm
        else:
            raise ValueError(f'Machine learning algorithm: {algorithm} is not available.')

        if forecast_time_span in ['1d', '5d', '1mo', '6mo', '1y']:
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
            # About 45 hours in a 5-day trading period
            self.steps = 45
            self.granularity = '1h'
        if forecast_time_span == '1mo':
            # 30 days in a month
            self.steps = 30
            self.granularity = '1d'
        if forecast_time_span == '6mo':
            # 6 months has 26 weeks x 5 trading days
            self.steps = 130
            self.granularity = '1d'
            self.delta_days = 4000
        if forecast_time_span == '1y':
            # 1 year has 52 weeks x 5 trading days
            self.steps = 260
            self.granularity = '1d'
            self.delta_days = 4000

        self.training_segment = self.seg_ratio * self.steps

    def get_mse(self):
        model = self.__train()
        prediction = self.__predict(model)
        mse = mean_squared_error(self.y_test, prediction[0])
        return mse

    def __train(self):
        model = None
        if self.algorithm == 'randomforest':
            model = self.__random_forest()
        if self.algorithm == 'lstm':
            model = self.__lstm()
        return model

    def __random_forest(self):
        delta = datetime.timedelta(days=self.delta_days)
        start_date = date.today() - delta
        end_date = date.today()
        data = yf.download(self.symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                           interval=self.granularity)
        self.data = data
        price_data = self.data.iloc[:]['Open'].values

        # Limit amount of data points. Too much data causes increased training time.
        if len(price_data) >= self.data_points:
            price_data = self.data.iloc[:]['Open'].values[-self.data_points:]
        else:
            price_data = self.data.iloc[:]['Open'].values[:]

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
            x = np.array(x)
            y = np.array(y)
            return x, y

        self.x_train, self.y_train = create_dataset(price_data[0:-(self.training_segment + self.steps)])
        self.x_test = np.array(price_data[-(self.training_segment + self.steps): -self.steps]).reshape(1, -1)
        self.y_test = np.array(price_data[-self.steps:])
        # self.x_train, self.y_train = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
        model = RandomForestRegressor(max_depth=self.max_depth, random_state=123, n_estimators=self.n_estimators,
                                      max_features=self.max_features)
        model.fit(self.x_train, self.y_train)

        return model

    def __lstm(self):
        model = None
        return model

    def __predict(self, model):
        prediction = self.x_test

        for i in range(self.steps):
            prediction = np.append(prediction, model.predict(prediction))
            prediction = prediction[-self.training_segment:].reshape(1, -1)
        return prediction[:, -self.steps:]
