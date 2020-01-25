from files.views import status, load_data
from django.urls import path

urlpatterns = [
    path('status', status),
    path('data', load_data),
]