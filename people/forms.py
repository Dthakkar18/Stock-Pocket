from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

# not using this form (created my own custom one)
class addStockForm(forms.Form):
    company_name = forms.CharField()
    company_ticker = forms.CharField()
    shares = forms.FloatField()
    avg_share_price = forms.FloatField()

# not using this form (created my own custom one)
class updateStockForm(forms.Form):
    company_ticker = forms.CharField()
    shares = forms.FloatField()
    avg_share_price = forms.FloatField()

# not using this form (created my own custom one)
class deleteStockForm(forms.Form):
    company_ticker = forms.CharField()

# not using this form (created my own custom one)
class detailStockForm(forms.Form):
    company_ticker = forms.CharField()

# not using this form (created my own custom one)
class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
