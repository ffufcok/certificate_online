from django import forms
from .models import Info


class OrderForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('surname', 'name', 'father', 'class_letter', 'email', 'date')
