from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
    path('jet_api/', include('jet_django.urls')),
    path('', include('order.urls')),
    path('register/', include('organisations.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='order/logout.html'), name='logout'),
    path('profile/', include('organisations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
