from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('queues/', include('queues.urls')),
    path('users/', include('users.urls')),
    path('departments/', include('departments.urls'))
]
