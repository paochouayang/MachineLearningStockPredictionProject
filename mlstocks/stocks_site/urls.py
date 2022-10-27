from django.urls import path
from . import views
from stocks_site.views import Login, ForgotPass, CreateAccount, Main, ForgotPassEmailDone, ForgotPassDone


app_name = 'stocks_site'

urlpatterns = [
    path('',views.user_login,name='login'),
    path('forgetPass/<str:uidb64>/<str:token>/', ForgotPass.as_view(), name="forgetPass"),
    path('forgotPassEmail', views.forgotPassEmail, name="forgotPassEmail"),
    path('createAccount', views.register, name="createAccount"),
    path('createAccountDone', views.CreateAccountDone.as_view(),name="createAccountDone"),
    path('main', views.stockPredict, name="main"),
    path('forgotPassEmailDone', ForgotPassEmailDone.as_view(), name="forgotPassEmailDone"),
    path('forgotPassDone', ForgotPassDone.as_view(), name="forgotPassDone")
]
