from files.views import status, load_data, upload, download
from django.urls import path

urlpatterns = [
    path('status', status),
    path('upload', upload),
    path('download/<str:key_file>', download),
    path('data', load_data),
]