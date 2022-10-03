from django.shortcuts import render, redirect
from django.views import View
from stocks_site.models import  Users

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,'stocks_site/login.html')
class ForgotPass(View):
    def get(self, request):
        return render(request,'stocks_site/forgetPass.html')
class CreateAccount(View):
    def get(self,request):
        return render(request,'stocks_site/createAccount.html')

class Main(View):
    def get(self,request):
        return render(request,'stocks_site/main.html')