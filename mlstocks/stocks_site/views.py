from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, StocksForm, ForgotPassForm
import requests, json


# Create your views here.
class Login(View):
    def get(self,request):
        return render(request,'stocks_site/login.html')

class CreateAccount(View):
    def get(self,request):
        return render(request,'stocks_site/createAccount.html')
class CreateAccountDone(View):
    def get(self,request):
        return render(request,'stocks_site/createAccountDone.html')

class Main(View):
    def get(self,request):
        return render(request,'stocks_site/main.html')

class ForgotPass(View):
        def get(self, request):
            if request.method == 'POST':
                forgotform = ForgotPassForm(request.POST)
            else:
                forgotform = ForgotPassForm()
            return render(request, 'stocks_site/forgetPass.html', {'forgotform': forgotform})

@login_required
def stockPredict(request):
    if request.method == 'POST':
        stockForm = StocksForm(request.POST)
        if stockForm.is_valid(): 
            input = stockForm.cleaned_data
            symbol = {'ticker':input['ticker']}
            response = requests.get(f'http://127.0.0.1:8000/api/', params=symbol)
            response_dict = json.loads(response.text)

            graphic = response_dict['Prediction']
            
            return render(request, 'stocks_site/main.html', {'graphic':graphic, 'stockForm': stockForm})
    else:
        stockForm = StocksForm()
    return render(request, 'stocks_site/main.html', {'stockForm': stockForm})
    

def user_login(request):
    message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                        username=cd['username'],
                                        password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/main')
            else:
                message = "Invalid Username/Password"
        else:
            message = "Invalid Username/Password"
    else:
        form = LoginForm()
    return render(request, 'stocks_site/login.html', {'form': form, 'message': message})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                            'stocks_site/createAccountDone.html')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                    'stocks_site/createAccount.html',
                    {'user_form': user_form})

def logout_view(request):
    logout(request)
    return redirect('/')