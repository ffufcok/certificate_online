from django import forms
from .models import Info, Schools

SCHOOL_CHOICES_1 = [
    Schools.objects.values_list('name')
]

SCHOOL_CHOICES = []

for i in range(len(SCHOOL_CHOICES_1)):
    st = str(SCHOOL_CHOICES_1[i])
    final = st[st.find("'") + 1: st.rfind("'")]
    SCHOOL_CHOICES.append((i, final))


class OrderForm(forms.Form):
    surname = forms.CharField(label='Фамилия', max_length=100)
    name = forms.CharField(label='Имя', max_length=100)
    father = forms.CharField(label='Отчество', max_length=100)
    class_letter = forms.CharField(label='Класс', max_length=10)
    email = forms.EmailField(label='Электронная почта')
    schools = forms.ChoiceField(choices=SCHOOL_CHOICES)