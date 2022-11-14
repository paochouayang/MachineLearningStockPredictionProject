from base64 import encode
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stockPredict import Stocks

class StockPredictions(APIView):
    def get(self, request):
        usage = request.GET.get('usage')

        stock_obj = Stocks(request.GET.get('ticker'), algorithm=request.GET.get('algorithm'),
                           forecast_time_span=request.GET.get('forecast'))

        if usage == 'forecast':
            stock_obj.forecast()
        if usage == 'test':
            stock_obj.forecast_test()

        graphic = stock_obj.plot
        mlResponse = {"Prediction" : graphic}
        return Response(mlResponse, status=status.HTTP_200_OK)
