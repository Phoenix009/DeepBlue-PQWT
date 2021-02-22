from django.urls import path
from . import views

app_name='departments'
urlpatterns = [
    path('', views.view_departments, name='view_departments'),
    path('reorder', views.reorder_departments, name='reorder_departments'),
]