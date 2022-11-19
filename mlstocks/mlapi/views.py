from base64 import encode
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stockPredict import Stocks
from .apps import MlapiConfig

class StockPredictions(APIView):
    def get(self, request):
        usage = request.GET.get('usage')
        model = None
        algorithm = request.GET.get('algorithm')
        ticker = request.GET.get('ticker')
        forecast = request.GET.get('forecast')

        if algorithm == 'lstm' and forecast == '1d':
            model = MlapiConfig.lstm_1d_model
        if algorithm == 'lstm' and forecast == '5d':
            model = MlapiConfig.lstm_5d_model
        if algorithm == 'lstm' and forecast == '1mo':
            model = MlapiConfig.lstm_1mo_model
        if algorithm == 'randomforest' and forecast == '1d':
            model = MlapiConfig.rf_1d_model
        if algorithm == 'randomforest' and forecast == '5d':
            model = MlapiConfig.rf_5d_model
        if algorithm == 'randomforest' and forecast == '1mo':
            model = MlapiConfig.rf_1mo_model

        stock_obj = Stocks(ticker, algorithm=algorithm, forecast_time_span=forecast, model=model)

        if usage == 'forecast':
            stock_obj.forecast()
        if usage == 'test':
            stock_obj.forecast_test()

        graphic = stock_obj.plot
        mlResponse = {"Prediction" : graphic}
        return Response(mlResponse, status=status.HTTP_200_OK)
