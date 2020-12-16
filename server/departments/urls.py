from django.urls import path
from . import views

app_name='departments'
urlpatterns = [
    path('view_queues/', views.view_queues, name='view_queues')
]