from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import OrderForm
from django.utils import timezone


def homepage(request):
    return render(request, 'order/main.html', {})


def orderpage(request):
    if request.method in ('GET', 'POST'):
        send_mail('Subject of the Email', 'Работает!', 'tol063115@gmail.com', ['tol063115@gmail.com'])
    return render(request, 'order/main.html', {})


def new_order(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            editable = form.save(commit=False)
            editable.date = timezone.now()
            form.save()
    return render(request, 'order/new_order.html', {'form': form})
