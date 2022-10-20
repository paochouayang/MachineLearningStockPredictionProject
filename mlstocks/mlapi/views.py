from base64 import encode
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .stockPredict import Stocks

class StockPredictions(APIView):
    def get(self, request):
        stock_obj = Stocks(request.GET.get('ticker'), algorithm='randomforest', forcast_time_span='5d')
        stock_obj.forcast_test()
        graphic = stock_obj.plot
        mlResponse = {"Prediction" : graphic}
        return Response(mlResponse, status=status.HTTP_200_OK)
