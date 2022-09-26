from django.shortcuts import render
from django.views import View

# Create your views here.
def login_view(request):
    return render(request,'stocks_site/login.html')

def forgetPass(request):
        return render(request,'stocks_site/forgetPass.html')

def createAccount(request):
    return render(request,'stocks_site/createAccount.html')