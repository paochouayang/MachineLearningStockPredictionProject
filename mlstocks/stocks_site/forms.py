from django import forms
from django.forms import Form, ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User

class LoginForm(Form):
    username = forms.CharField(label='', 
                                widget=forms.TextInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingInput',
                                    'placeholder': 'UserName or Email'
                                }))
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Password'
                                }))

class ForgotPassForm(Form):
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Password'
                                }))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Confirm Password'
                                }))
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class ForgotPassEmailForm(Form):
    email = forms.CharField(label='',
                            widget=forms.EmailInput(attrs={
                            'class': "form-control",
                            'id': 'floatingInput',
                            'placeholder': 'name@example.com'
                            }))

class UserRegistrationForm(ModelForm):

    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Password'
                                }))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Repeat Password'
                                }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'UserName'
                }),
            'first_name': TextInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'FirstName'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'LastName'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'name@example.com'
            })
        }
        labels = {
            'username': "",
            'first_name': "",
            'last_name': "",
            'email': ""
        }
        help_texts = {
            'username':None,

        }

    def clean_password2(self):
        cd = self.cleaned_data
        if self.all_required(cd):
            raise forms.ValidationError('All fields required')
        if self.account_exists(cd):
            raise forms.ValidationError('Username or email already exists.')
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def account_exists(self, cd):
        try:
            User.objects.get(username=cd['username'])
        except User.DoesNotExist:
            try:
                User.objects.get(email=cd['email'])
            except User.DoesNotExist:
                return False
        return True    

    def all_required(self, cd):
        for k,v in cd.items():
            if v == '':
                return True
        return False

class StocksForm(Form):
    ticker = forms.CharField()
    ALGO = (
        ('lstm', 'LSTM'),
        ('randomforest', 'Random Forest')
    )
    INTERVAL = (
        ('1d', '1 day'),
        ('5d', '5 days'),
        ('1mo', '1 month')
    )
    USAGE = (
        ('forecast', 'Forecast'),
        ('test', 'Test Algorithm')
    )
    algorithm = forms.ChoiceField(choices=ALGO)
    forecast = forms.ChoiceField(choices=INTERVAL)
    usage = forms.ChoiceField(choices=USAGE)

class AccountManagementForm(ModelForm):    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = { 
            'first_name' : TextInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'FirstName'
            }),
            'last_name' : TextInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'LastName'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'name@example.com'
            })
        }
        labels = {
            'first_name': "",
            'last_name': "",
            'email': ""
        }
