from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('queues/', include('queues.urls')),
    path('users/', include('users.urls')),
    path('departments/', include('departments.urls')),
    path('patients/', include('patients.urls')),
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(
        template_name = 'users/password_reset.html'),
        name = 'password_reset'
    ),
    path('password-reset/done/', 
    auth_views.PasswordResetDoneView.as_view(
        template_name = 'users/password_reset_done.html'),
        name = 'password_reset_done'
    ),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
    ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
    ),
      name='password_reset_complete'),
]
