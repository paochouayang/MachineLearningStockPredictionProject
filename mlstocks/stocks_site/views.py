import smtplib
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .forms import LoginForm, UserRegistrationForm, StocksForm, ForgotPassForm, ForgotPassEmailForm
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
        def get(self, request, uidb64, token):
            forgotform = ForgotPassForm()
            return render(request, 'stocks_site/forgetPass.html', {'forgotform': forgotform})
        
        def post(self, request, uidb64, token):
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except:
                return redirect('/')
            if request.method == 'POST' and user is not None and default_token_generator.check_token(user, token):
                forgotform = ForgotPassForm(request.POST)
                if forgotform.is_valid():
                    password = forgotform.cleaned_data
                    user.set_password(password['password'])
                    user.save()
                    return redirect('stocks_site:forgotPassDone')
                return render(request, 'stocks_site/forgetPass.html', {'forgotform': forgotform})
            return redirect('/')

class ForgotPassEmailDone(View):
    def get(self,request):
        return render(request, 'stocks_site/forgotPassEmailDone.html')

class ForgotPassDone(View):
    def get(self,request):
        return render(request, 'stocks_site/forgotPassDone.html')

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

def forgotPassEmail(request):
    if request.method == "POST":
        emailResetForm = ForgotPassEmailForm(request.POST)
        if emailResetForm.is_valid():
            data = emailResetForm.cleaned_data['email']
            user = User.objects.get(email=data)
            if user is not None and user.is_active:
                subject = "Password Reset Requested"
                email_template = "stocks_site/resetEmail.txt"
                email_info = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'MLStocks',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http'
					}
                email = render_to_string(email_template, email_info)
                try:
                    send_mail(subject, email, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email], fail_silently=False)
                except smtplib.SMTPException: # Will need to change because it will error on emails that do not exist
                    return HttpResponse("Email not sent")
                return redirect('stocks_site:forgotPassEmailDone')
    emailResetForm = ForgotPassEmailForm()
    return render(request, 'stocks_site/forgotPassEmail.html', {'emailResetForm': emailResetForm})

