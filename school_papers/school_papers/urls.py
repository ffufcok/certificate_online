from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
    path('jet_api/', include('jet_django.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='order/logout.html'), name='logout'),
    path('profile/', include('organizations.urls')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='order/password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='order/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='order/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='order/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('', include('order.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
