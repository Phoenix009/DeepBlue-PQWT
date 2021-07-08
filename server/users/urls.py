from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from core import settings
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(template_name="users/login.html"),name="login"),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},name="logout"),
    path('view_staff/<int:pk>', views.view_staff , name="view_staff"),
    path('create_staff/<int:pk>', views.create_staff , name="create_staff"),
]
