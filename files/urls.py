from files.views import status, load_data, upload
from django.urls import path

urlpatterns = [
    path('status', status),
    path('upload', upload),
    path('data', load_data),
]