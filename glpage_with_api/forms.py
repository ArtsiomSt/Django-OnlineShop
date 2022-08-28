from django import forms
from .models import buy, nomerz, category, OrderModel
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class User_login_form(AuthenticationForm):
    username = forms.CharField(label='name', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='pass', widget=forms.PasswordInput(attrs={"class": "form-control"}))

class UserRegistration(UserCreationForm):
    username = forms.CharField(label='name', widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='pass', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='proof', widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class buyform(forms.Form):
    title = forms.CharField(max_length=50, label='Название', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Котент', required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
    price = forms.FloatField(label='Цена', widget=forms.NumberInput(attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(queryset=category.objects.all(), label='Категория', empty_label='Choose', widget=forms.Select(attrs={"class": "form-control"}))

    def clean_title(self):
        title=self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValueError('Nazvanie ne dlozno nachinatsyz s 123456789')
        return title

class nomer(forms.ModelForm):
    class Meta:
        model = nomerz
        fields = ["num"]

class boolform(forms.Form):
    yorn = forms.BooleanField(label='Добавить в корзину?')

class Searchform(forms.Form):
    search = forms.CharField(max_length=50, label='Поиск', widget=forms.TextInput(attrs={"class": "form-control"}))

class OrderModelform(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['ordered_by_name', 'ordered_by_phone', 'transport', 'address']
