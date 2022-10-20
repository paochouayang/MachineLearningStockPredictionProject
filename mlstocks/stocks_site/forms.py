from django import forms
from django.forms import Form, ModelForm, TextInput, EmailInput
from django.contrib.auth.models import User

class LoginForm(Form):
    username = forms.CharField(label='', 
                                widget=forms.TextInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingInput',
                                    'placeholder': 'UserName'
                                }))
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingPassword',
                                    'placeholder': 'Password'
                                }))

class ForgotPassForm(Form):
    username = forms.CharField(label='',
                                widget=forms.TextInput(attrs={
                                    'class': "form-control",
                                    'id': 'floatingInput',
                                    'placeholder': 'UserName'
                                }))
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
        fields = ('username', 'first_name', 'email')
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
            'email': EmailInput(attrs={
                'class': "form-control",
                'id': 'floatingInput',
                'placeholder': 'name@example.com'
            })
        }
        labels = {
            'username': "",
            'first_name': "",
            'email': ""
        }
        help_texts = {
            'username':None,

        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class StocksForm(Form):
    ticker = forms.CharField()