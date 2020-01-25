from files.views import ListUploadAndDeleteFile, DownloadFile, ProcessCsvData
from django.urls import path

urlpatterns = [
    path('list', ListUploadAndDeleteFile.as_view()),
    path('upload', ListUploadAndDeleteFile.as_view()),
    path('download/<str:key_file>', DownloadFile.as_view()),
    path('delete/<str:key_file>', ListUploadAndDeleteFile.as_view()),
    path('data/<str:key_file>', ProcessCsvData.as_view()),
]