from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('makeorder/', views.new_order, name='new_order'),
]
