from django import forms
from .models import Schools, Info


class OrderForm(forms.ModelForm):
    surname = forms.CharField(label='Фамилия', max_length=100)
    name = forms.CharField(label='Имя', max_length=100)
    father = forms.CharField(label='Отчество', max_length=100)
    class_letter = forms.CharField(label='Класс', max_length=10)
    email = forms.EmailField(label='Электронная почта')
    schools = forms.ChoiceField(choices=[(choice, choice) for choice in Schools.objects.all()])

    class Meta:
        model = Info
        fields = ['surname', 'name', 'father', 'class_letter', 'email', 'schools']
