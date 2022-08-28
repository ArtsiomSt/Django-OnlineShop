from django import forms
from .models import *

class QAform(forms.Form):
    answer = forms.CharField(label = 'Ответ',widget=forms.TextInput(attrs={"class": "form-control"}))
    yorn = forms.BooleanField(label='Отвечено',  widget=forms.CheckboxInput, required=False)
