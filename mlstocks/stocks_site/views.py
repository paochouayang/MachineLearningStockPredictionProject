from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request,'stocks_site/login.html')

def forget_pass(request):
    return render(request,'stocks_site/forgetPass.html')