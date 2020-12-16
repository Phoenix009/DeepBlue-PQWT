from django.urls import path
from . import views

app_name='queues'
urlpatterns = [
    path('', views.index , name = 'index'),
    path('<str:room_name>/', views.room, name = 'room'),
    path('add-patient/<str:room_name>/', views.add_patient, name = 'add_patient'),
    path('patients/data/', views.get_patients_data, name = 'get_patients_data'),
]