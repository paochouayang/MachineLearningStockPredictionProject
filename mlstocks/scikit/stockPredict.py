import datetime
from datetime import date
import yfinance as yf
import numpy as np
import numpy
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd


class Stocks:
    def __init__(self, symbol, algorithm, forecast_time_span):
        self.symbol = symbol
        self.algorithm = algorithm
        self.data_points = 1000
        self.forecast_time_span = forecast_time_span
        self.delta_days = 720
        self.seg_ratio = None
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
            self.seg_ratio = 1
        if forecast_time_span == '5d':
            # About 35 hours in a 5-day trading period
            self.steps = 35
            self.granularity = '1h'
            self.seg_ratio = 2
        if forecast_time_span == '1mo':
            # 21 trading days in a month
            self.steps = 21
            self.granularity = '1d'
            self.seg_ratio = 2
        """
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
        """
        self.training_segment = self.seg_ratio * self.steps

    def forecast(self):
        model = self.__train()
        price_data = self.data.iloc[:]['Open'].values
        x_predict = np.array(price_data[-self.training_segment:]).reshape(1, -1)
        prediction = self.__predict(model, x_predict)

        # Generate future dates to plot against prediction
        def extend_x_axis():
            td_param = [*self.granularity]
            delta = pd.Timedelta(int(td_param[0]), td_param[1])
            start_point = self.data.index[-1:][0]
            future_points_lst = []
            current_point = start_point
            for i in range(self.steps):
                current_point = current_point + delta
                if self.granularity == '1h':
                    # skip date times that land on weekends or outside of trading hours
                    while current_point.weekday() >= 5 or current_point.hour < 8 \
                            or current_point.hour >= 15:
                        current_point = current_point + delta
                if self.granularity == '1d':
                    while current_point.weekday() >= 5:
                        current_point = current_point + delta
                future_points_lst.append(current_point)
            return future_points_lst

        plt.plot(extend_x_axis(), prediction[0], label='Prediction', color='red')
        self.data['Open'][-(self.training_segment + self.steps):].plot(label='Historical Data', color='blue')
        plt.title('Prediction for stock: ' + self.symbol)
        plt.legend(loc='lower left')
        plt.show()
        return prediction

    def forecast_test(self):
        model = self.__train()
        prediction = self.__predict(model, self.x_test)
        mse = mean_squared_error(self.y_test, prediction[0])
        print(f"Mean Squared Error: {mse}")
        plt.plot(self.data.index[-self.steps:], prediction[0], label='Prediction data', color='red')
        self.data['Open'][-(self.training_segment + self.steps):-self.steps].plot(label='Training data', color='blue')
        self.data['Open'][-self.steps:].plot(label='Testing data', color='green')
        plt.title('Prediction for stock: ' + self.symbol)
        plt.legend(loc='lower left')
        plt.show()
        return prediction

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

        # Method to create training
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
        model = None
        if self.forecast_time_span == '1d':
            model = RandomForestRegressor(max_depth=10, random_state=123, n_estimators=50, max_features='log2')
        if self.forecast_time_span == '5d':
            model = RandomForestRegressor(max_depth=10, random_state=123, n_estimators=50, max_features=None)
        if self.forecast_time_span == '1mo':
            model = RandomForestRegressor(max_depth=10, random_state=123, n_estimators=100, max_features='sqrt')
        model.fit(self.x_train, self.y_train)

        return model

    def __lstm(self):
        model = None
        return model

    def __predict(self, model, data):
        prediction = data

        for i in range(self.steps):
            prediction = np.append(prediction, model.predict(prediction))
            prediction = prediction[-self.training_segment:].reshape(1, -1)
        return prediction[:, -self.steps:]
