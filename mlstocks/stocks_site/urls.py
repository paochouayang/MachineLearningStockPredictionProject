from django.urls import path
from . import views


app_name = 'stocks_site'

urlpatterns = [
    path('',views.login_view,name='login'),
    path('forgetPass', views.forgetPass,name="forgetPass"),
]
