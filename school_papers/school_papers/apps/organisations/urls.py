from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='registration'),
    path('user', views.profile, name='profile')
]
