from django.urls import path
from . import views
from stocks_site.views import Login, ForgotPass, CreateAccount


app_name = 'stocks_site'

urlpatterns = [
    path('',Login.as_view(),name='login'),
    path('forgetPass', ForgotPass.as_view(),name="forgetPass"),
    path('createAccount', CreateAccount.as_view(), name="createAccount")
]
