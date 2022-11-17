from django.urls import path
from . import views


app_name = 'stocks_site'

urlpatterns = [
    path('',views.user_login,name='login'),
    path('forgetPass/<str:uidb64>/<str:token>/', views.ForgotPass.as_view(), name="forgetPass"),
    path('forgotPassEmail', views.forgotPassEmail, name="forgotPassEmail"),
    path('createAccount', views.register, name="createAccount"),
    path('createAccountDone', views.CreateAccountDone.as_view(),name="createAccountDone"),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateAccount.as_view(), name="activateAccount"),
    path('main', views.stockPredict, name="main"),
    path('forgotPassEmailDone', views.ForgotPassEmailDone.as_view(), name="forgotPassEmailDone"),
    path('forgotPassDone', views.ForgotPassDone.as_view(), name="forgotPassDone"),
    path('manageAccount', views.manageAccount, name="manageAccount"),
    path('RandomForestDis', views.RandomForestDis.as_view(), name="randomForestDis"),
    path('LSTMDis', views.LSTMDis.as_view(), name="LSTMDis"),
    path('update/<str:uidb64>/<str:token>/<str:uidb642>/', views.UpdateAccount.as_view(), name="updateEmail")
]
