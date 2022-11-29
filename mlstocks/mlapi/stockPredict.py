import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
from datetime import date
import yfinance as yf
import numpy as np
from io import BytesIO
import base64
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


class Stocks:
    def __init__(self, symbol, forecast_time_span, algorithm=None, model=None):
        self.symbol = symbol
        self.algorithm = algorithm
        self.data_points = 1000
        self.forecast_time_span = forecast_time_span
        self.delta_days = 720
        self.model = model
        self.start = None
        self.end = None
        self.steps = None
        self.data = None
        self.lstm_x_test = None
        self.lstm_y_test = None
        self.rf_x_test = None
        self.rf_y_test = None
        self.steps = None
        self.plot = None

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
            self.rf_seg_ratio = 3
            self.lstm_seg_ratio = 4
        if forecast_time_span == '5d':
            # About 35 hours in a 5-day trading period
            self.steps = 35
            self.granularity = '1h'
            self.rf_seg_ratio = 2
            self.lstm_seg_ratio = 4
        if forecast_time_span == '1mo':
            # 21 trading days in a month
            self.steps = 21
            self.granularity = '1d'
            self.rf_seg_ratio = 3
            self.lstm_seg_ratio = 4

        self.rf_training_segment = self.rf_seg_ratio * self.steps
        self.lstm_training_segment = self.lstm_seg_ratio * self.steps

        self.__create_data()

    def forecast(self, model, algorithm):
        if algorithm in ['randomforest', 'lstm']:
            self.algorithm = algorithm
            if algorithm == 'lstm':
                training_segment = self.lstm_training_segment
            if algorithm == 'randomforest':
                training_segment = self.rf_training_segment
        else:
            raise ValueError(f'Machine learning algorithm: {algorithm} is not available.')
        plt.cla()
        price_data = self.data.iloc[:]['Open'].values
        x_predict = np.array(price_data[-training_segment:]).reshape(1, -1)
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

        plt.plot(extend_x_axis(), prediction, label='Prediction', color='red')
        self.data['Open'][-(training_segment + self.steps):].plot(label='Historical Data', color='blue')
        plt.xlabel("Date")
        plt.ylabel("Price USD")
        plt.grid()
        plt.legend(loc='lower left')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        self.plot = graphic
        return prediction

    """
    def forecast_test(self):
        plt.cla()
        model = self.model
        prediction = self.__predict(model, self.x_test)
        self.data['Open'][-(self.training_segment + self.steps):-self.steps].plot(label='Training data')
        self.data['Open'][-self.steps:].plot(label='Testing data')
        plt.plot(self.data.index[-self.steps:], prediction, label='Prediction data')
        plt.legend(loc='lower left')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        self.plot = graphic
        return prediction
    """

    def get_mse(self, model, algorithm):
        if algorithm in ['randomforest', 'lstm']:
            self.algorithm = algorithm
        else:
            raise ValueError(f'Machine learning algorithm: {algorithm} is not available.')
        if algorithm == 'lstm':
            prediction = self.__predict(model, self.lstm_x_test)
            mse = mean_squared_error(self.lstm_y_test, prediction)
            return mse
        if algorithm == 'randomforest':
            prediction = self.__predict(model, self.rf_x_test)
            mse = mean_squared_error(self.rf_y_test, prediction)
            return mse

    def __create_data(self):
        self.__download_data()
        self.__create_lstm_data()
        self.__create_random_forest_data()

    def __download_data(self):
        delta = datetime.timedelta(days=self.delta_days)
        start_date = date.today() - delta
        end_date = date.today()
        data = yf.download(self.symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'),
                           interval=self.granularity)
        self.data = data

    def __create_random_forest_data(self):
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
            for i in range(self.rf_training_segment, len(dataframe)):
                x.append(dataframe[i - self.rf_training_segment:i])
                y.append(dataframe[i])
            x = np.array(x)
            y = np.array(y)
            return x, y

        #self.rf_x_train, self.rf_y_train = create_dataset(price_data[0:-(self.training_segment + self.steps)])
        self.rf_x_test = np.array(price_data[-(self.rf_training_segment + self.steps): -self.steps]).reshape(1, -1)
        self.rf_y_test = np.array(price_data[-self.steps:])

    def __create_lstm_data(self):
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
            dataframe = MinMaxScaler(feature_range=(0, 1)).fit_transform(dataframe.reshape(-1, 1))
            x = []
            y = []
            for i in range(self.lstm_training_segment, len(dataframe)):
                x.append(dataframe[i - self.lstm_training_segment:i])
                y.append(dataframe[i])
            x = np.array(x)
            y = np.array(y)
            return x, y

        #self.lstm_x_train, self.lstm_y_train = create_dataset(price_data[0:-(self.training_segment + self.steps)])
        self.lstm_x_test = np.array(price_data[-(self.lstm_training_segment + self.steps): -self.steps]).reshape(1, -1)
        self.lstm_y_test = np.array(price_data[-self.steps:])

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
                x_predict = prediction[-self.lstm_training_segment:].reshape(1, -1)
            if self.algorithm == 'randomforest':
                next_predict = model.predict(x_predict)
                prediction = np.append(prediction, next_predict)
                x_predict = prediction[-self.rf_training_segment:].reshape(1, -1)

        return prediction[-self.steps:]
