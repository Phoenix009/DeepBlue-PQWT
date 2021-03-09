from django.urls import path
from . import views

app_name='departments'
urlpatterns = [
    path('', views.view_departments, name='view_departments'),
    path('reorder', views.reorder_departments, name='reorder_departments'),
    path('create-department', views.create_department, name="create_department"),
    path('update-department/<int:pk>', views.update_department, name="update_department"),
    path('delete-department/<int:pk>', views.delete_department, name="delete_department"),
]