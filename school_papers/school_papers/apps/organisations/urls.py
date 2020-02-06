from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='registration'),
    path('user', views.profile, name='profile'),
    path('(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
         name='activate')

]
