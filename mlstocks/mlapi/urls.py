from django.urls import path
from . import views

app_name='mlapi'

urlpatterns = [
    path('', views.StockPredictions.as_view(), name='StockPredictions'),
]
