from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('makeorder/', views.new_order, name='new_order'),
    path('confirm/<str:user_email>/<str:token>', views.confirm,
         name='confirm'),
    path('decline/<str:user_email>/<str:token>', views.decline,
         name='decline'),

]
