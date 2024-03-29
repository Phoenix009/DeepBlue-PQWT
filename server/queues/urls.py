from django.urls import path
from . import views

app_name='queues'
urlpatterns = [
    path('', views.index , name = 'index'),
    path('<str:room_name>/', views.room, name = 'room'),
    path('add-patient/<str:room_name>/', views.add_patient, name = 'add_patient'),
    path('patients-data/stats/', views.stats, name = 'stats'),
    # path('patients/data/', views.get_patients_data, name = 'get_patients_data'),
    path('patients/complete/', views.complete_patient, name = 'complete_patient'),
    path('patients/remove/', views.remove_patient, name = 'remove_patient'),
    path('patients/wait-time/<str:token>/', views.view_wait_time, name = 'view_wait_time'),
    path('qrcode/<str:room_name>/', views.open_qrcode, name = 'open_qrcode'),
    path('test/page', views.test_ui, name= 'test_ui'),
    path('token_visualizer/<int:pk>', views.token_visualizer, name='token_visualizer'),
]