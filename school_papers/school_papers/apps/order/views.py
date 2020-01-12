from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import OrderForm


def index(request):
    return HttpResponse('Hello World!')


def homepage(request):
    return render(request, 'order/main.html', {})


def orderpage(request):
    if request.method in ('GET', 'POST'):
        send_mail('Subject of the Email', 'Работает!', 'tol063115@gmail.com', ['tol063115@gmail.com'])
    return render(request, 'order/main.html', {})


def new_order(request):
    form = OrderForm()
    return render(request, 'order/new_order.html', {'form': form})
