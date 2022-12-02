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
from . import forms
import httpx, requests, json
from asgiref.sync import sync_to_async, async_to_sync
from .models import Tickers


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

class ForgotPass(View):
        def get(self, request, uidb64, token):
            forgotform = forms.ForgotPassForm()
            return render(request, 'stocks_site/forgetPass.html', {'forgotform': forgotform})
        
        def post(self, request, uidb64, token):
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except:
                return redirect('/')
            if request.method == 'POST' and user is not None and default_token_generator.check_token(user, token):
                forgotform = forms.ForgotPassForm(request.POST)
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

class RandomForestDis(View):
    def get(self,request):
        return render(request, 'stocks_site/RandomForestDis.html')

class LSTMDis(View):
    def get(self,request):
        return render(request, 'stocks_site/LSTMDis.html')

class ForgotPassDone(View):
    def get(self,request):
        return render(request, 'stocks_site/forgotPassDone.html')

class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except:
            return redirect('/')
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'stocks_site/activateAccount.html')
        return redirect('/')

class UpdateAccount(View):
    def get(self, request, uidb64, token, uidb642):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
            newEmail = str(urlsafe_base64_decode(uidb642), 'UTF-8')
        except:
            return redirect('/')
        if user is not None and default_token_generator.check_token(user, token):
            user.email = newEmail
            user.save()
            return render(request, 'stocks_site/updatedAccount.html')
        return redirect('/')

@login_required
def manageAccount(request):
    if request.method == "POST":
        account_form = forms.AccountManagementForm(request.POST)
        if account_form.is_valid():
            first_name = account_form.cleaned_data['first_name']
            last_name = account_form.cleaned_data['last_name']
            newEmail = account_form.cleaned_data['email']
            try:
                CurrentUser = User.objects.get(id=request.user.id)
            except:
                redirect('stocks_site:login')
            if CurrentUser.email != newEmail:
                try:
                    User.objects.get(email=newEmail)
                except:       
                    if CurrentUser.email != newEmail:
                        subject = "MLStocks Email Update"
                        email_template = "stocks_site/updateEmail.txt"
                        email_info = {
                            "email":newEmail,
                            'domain':'mlstocks-production.up.railway.app',
                            'site_name': 'MLStocks',
                            "uid": urlsafe_base64_encode(force_bytes(CurrentUser.pk)),
                            "user": CurrentUser,
                            'token': default_token_generator.make_token(CurrentUser),
                            'uidemail': urlsafe_base64_encode(force_bytes(newEmail)),
                            'protocol': 'http'
                            }
                        email = render_to_string(email_template, email_info)
                        try:
                            send_mail(subject, email, from_email=settings.EMAIL_HOST_USER, recipient_list=[newEmail], fail_silently=False)
                        except smtplib.SMTPException:
                            return HttpResponse("Email not sent")
                    CurrentUser.first_name = first_name
                    CurrentUser.last_name = last_name
                    CurrentUser.save()
                    message = 'Account updated successfully, email changes will require activation via the link sent to the new email.'
                    return render(request, 'stocks_site/manageAccount.html',
                        {'account_form': account_form, 'message': message})
                alert = 'Account already associated with that email'
                return render(request, 'stocks_site/manageAccount.html',
                        {'account_form': account_form, 'alert': alert})   
            else:
                CurrentUser.first_name = first_name
                CurrentUser.last_name = last_name
                CurrentUser.save()
                message = 'Account updated successfully.'
                return render(request, 'stocks_site/manageAccount.html',
                    {'account_form': account_form, 'message': message})
        alert = 'Invalid changes.'
        return render(request, 'stocks_site/manageAccount.html',
            {'account_form': account_form, 'alert': alert})
    else:
        account_form = forms.AccountManagementForm(initial={'username':request.user.username, 'first_name':request.user.first_name, 'last_name':request.user.last_name, 'email':request.user.email})
    return render(request,
                'stocks_site/manageAccount.html',
                {'account_form': account_form})

@sync_to_async
@login_required
@async_to_sync
async def stockPredict(request):
    if request.method == 'POST':
        stockForm = forms.StocksForm(request.POST)
        if stockForm.is_valid():
            input = stockForm.cleaned_data
            ticker = input['ticker']
            forecast = input['forecast']
            doesExist = await ticker_exists(ticker)

            if not doesExist:
                message = 'Ticker not available'
                return render(request, 'stocks_site/main.html', {'stockForm': stockForm, 'message': message})
            param = {
                'ticker': ticker,
                'forecast': forecast
            }

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f'https://mlstocks-production.up.railway.app/api/', params=param, timeout=None)
            except httpx.ReadTimeout:
                pass
            timespan = None
            if forecast == '1d':
                timespan = '1 Day'
            if forecast == '5d':
                timespan = '5 Day'
            if forecast == '1mo':
                timespan = '1 Month'
            try:
                response_dict = json.loads(response.text)

                graphic = response_dict['Prediction']
                description = await get_ticker_description(ticker)

                title = description + ' (' + ticker.upper() + ') - ' + timespan + ' Forecast'
                model_message = 'The ' + response_dict['bestAlgorithm'] + ' algorithm was chosen for this prediction based ' \
                                                                          'on best accuracy from past performance.'

                return render(request, 'stocks_site/main.html', {'graphic': graphic, 'stockForm': stockForm,
                                                                 'model_message': model_message, 'title': title})
            except json.decoder.JSONDecodeError:
                message = "There is not enough historical data for this stock to make a " + timespan + ' forecast.'
                return render(request, 'stocks_site/main.html', {'stockForm': stockForm, 'message': message})
    else:
        stockForm = forms.StocksForm()
    return render(request, 'stocks_site/main.html', {'stockForm': stockForm})

@sync_to_async
def ticker_exists(inputTicker):
    return Tickers.objects.filter(ticker=inputTicker).exists()

@sync_to_async
def get_ticker_description(inputTicker):
    ticker = Tickers.objects.get(ticker=inputTicker)
    return ticker.description
    
def user_login(request):
    message = ""
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
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
        form = forms.LoginForm()
    return render(request, 'stocks_site/login.html', {'form': form, 'message': message})

def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.is_active = False

            new_user.save()

            subject = "MLStocks Account Activation"
            email_template = "stocks_site/activationEmail.txt"
            email_info = {
                "email":new_user.email,
                'domain':'mlstocks-production.up.railway.app',
                'site_name': 'MLStocks',
                "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "user": new_user,
                'token': default_token_generator.make_token(new_user),
                'protocol': 'http'
                }
            email = render_to_string(email_template, email_info)
            try:
                send_mail(subject, email, from_email=settings.EMAIL_HOST_USER, recipient_list=[new_user.email], fail_silently=False)
            except smtplib.SMTPException:
                return HttpResponse("Email not sent")

            return redirect('stocks_site:createAccountDone')
    else:
        user_form = forms.UserRegistrationForm()
    return render(request,
                    'stocks_site/createAccount.html',
                    {'user_form': user_form})

def logout_view(request):
    logout(request)
    return redirect('/')

def forgotPassEmail(request):
    if request.method == "POST":
        emailResetForm = forms.ForgotPassEmailForm(request.POST)
        if emailResetForm.is_valid():
            data = emailResetForm.cleaned_data['email']
            try:
                user = User.objects.get(email=data)
            except:
                return redirect('stocks_site:forgotPassEmailDone')
            if user is not None and user.is_active:
                subject = "Password Reset Requested"
                email_template = "stocks_site/resetEmail.txt"
                email_info = {
					"email":user.email,
					'domain':'mlstocks-production.up.railway.app',
					'site_name': 'MLStocks',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http'
					}
                email = render_to_string(email_template, email_info)
                try:
                    send_mail(subject, email, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email], fail_silently=False)
                except smtplib.SMTPException:
                    return redirect('stocks_site:forgotPassEmailDone')
                return redirect('stocks_site:forgotPassEmailDone')
    emailResetForm = forms.ForgotPassEmailForm()
    return render(request, 'stocks_site/forgotPassEmail.html', {'emailResetForm': emailResetForm})

