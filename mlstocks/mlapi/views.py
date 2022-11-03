from base64 import encode
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stockPredict import Stocks

class StockPredictions(APIView):
    def get(self, request):
        stock_obj = Stocks(request.GET.get('ticker'), algorithm='lstm', forecast_time_span='1d')
        stock_obj.forecast_test()
        #stock_obj.forecast()
        graphic = stock_obj.plot
        mlResponse = {"Prediction" : graphic}
        return Response(mlResponse, status=status.HTTP_200_OK)
