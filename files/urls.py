from files.views import status
from django.urls import path

urlpatterns = [
    path('status', status),
]