from base64 import encode
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stockPredict import Stocks
from .apps import MlapiConfig

class StockPredictions(APIView):
    def get(self, request):
        ticker = request.GET.get('ticker')
        forecast = request.GET.get('forecast')
        mse_vals = {}
        bestAlgorithm = ''
        model = None
        lstm_model = None
        rf_model = None

        if forecast == '1d':
            lstm_model = MlapiConfig.lstm_1d_model
            rf_model = MlapiConfig.rf_1d_model
        if forecast == '5d':
            lstm_model = MlapiConfig.lstm_5d_model
            rf_model = MlapiConfig.rf_5d_model
        if forecast == '1mo':
            lstm_model = MlapiConfig.lstm_1mo_model
            rf_model = MlapiConfig.rf_1mo_model

        stock_obj = Stocks(ticker, forecast_time_span=forecast)
        mse_vals['lstm'] = stock_obj.get_mse(lstm_model, 'lstm')
        mse_vals['randomforest'] = stock_obj.get_mse(rf_model, 'randomforest')
        mse_min = min(mse_vals.values())
        best_alg = [key for key in mse_vals if mse_vals[key] == mse_min]

        if best_alg[0] == 'lstm':
            stock_obj.forecast(lstm_model, 'lstm')
            bestAlgorithm = 'LSTM'
        if best_alg[0] == 'randomforest':
            stock_obj.forecast(rf_model, 'randomforest')
            bestAlgorithm = 'Random Forest'

        graphic = stock_obj.plot
        mlResponse = {"Prediction" : graphic,
                      'bestAlgorithm': bestAlgorithm}
        return Response(mlResponse, status=status.HTTP_200_OK)
