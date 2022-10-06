from django.urls import path
from . import views
from stocks_site.views import Login, ForgotPass, CreateAccount, Main


app_name = 'stocks_site'

urlpatterns = [
    path('',views.user_login,name='login'),
    path('forgetPass', ForgotPass.as_view(),name="forgetPass"),
    path('createAccount', views.register, name="createAccount"),
    path('createAccountDone', views.CreateAccountDone.as_view(),name="createAccountDone"),
    path('main', views.stockPredict, name="main"),
]
