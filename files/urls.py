from files.views import status, load_data, upload, download, list_files, delete_file
from django.urls import path

urlpatterns = [
    path('status', status),
    path('list/', list_files),
    path('upload', upload),
    path('download/<str:key_file>', download),
    path('delete/<str:key_file>', delete_file),
    path('data/<str:key_file>', load_data),
]