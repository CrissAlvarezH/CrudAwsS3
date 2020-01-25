from rest_framework.decorators import api_view
from django.http import HttpResponse
from os import remove
from rest_framework.response import Response
from testbackend.aws_s3_credentials import s3_data
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto3
import pandas as pd 
import logging


def get_s3_client():
    return boto3.client(
            service_name='s3',
            region_name= s3_data['region_name'],
            aws_access_key_id= s3_data['aws_access_key_id'],
            aws_secret_access_key= s3_data['aws_secret_access_key']
        )

@api_view(['GET'])
def status(request):
    return Response({'okay': True})

@api_view(['POST'])
def upload(request):
    s3Client = get_s3_client()

    file = request.FILES.get('file')

    if file:
        s3Client.upload_fileobj(
            file,  # File
            'testfilessimetrick',  # Name of bucket
            file.name #  Name of file in the bucket
        )

        return Response({ 'okay': True, 'file': file.name })
    
    return Response({ 'okay': False, 'error': 'File no puede ser nulo' })

@api_view(['GET'])
def download(request, key_file):
    s3Client = get_s3_client()

    # Save file temporaly 
    with open('./temp_files/temp.csv', 'wb') as file:
        s3Client.download_fileobj('testfilessimetrick', key_file, file)

    # Read file to send on response
    with open('./temp_files/temp.csv', 'rb') as f:
        filedata = f.read()

    response = HttpResponse(filedata, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (key_file)

    remove('./temp_files/temp.csv') # Delete file that will be send as response

    return response

@api_view(['GET'])
def load_data(request):
    data = pd.read_csv("./temp_files/test2.csv")

    # [ INIT ] FILTER COLUMNS WITH PARAMS
    filter_columns = []

    query_columns = request.query_params.get('columns')
    if query_columns:
        filter_columns = query_columns.split(',')

    try:
        data_result = data[filter_columns] if len(filter_columns) > 0 else data
    except Exception as e:
        return Response( { 'okay': False, 'error': str(e) } )
    # [ END ] FILTER COLUMNS WITH PARAMS

    # [ INIT ] SORTING VALUES
    ascending = True

    asc = request.query_params.get('asc')
    if asc:
        try:
            ascending = int(asc) > 0
        except Exception as e:
            return Response( { 'okay': False, 'error': 'El parametro \'asc\' debe ser entero' } )

    sort_columns = []
    query_sort_columns = request.query_params.get('sort')
    if query_sort_columns:
        sort_columns = query_sort_columns.split(',')

    try:
        data_result = data_result.sort_values(by=sort_columns, ascending=ascending) if len(sort_columns) > 0 else data_result
    except Exception as e:
        return Response( { 'okay': False, 'error': "La columna %s no existe"%(str(e)) } )
    # [ END ] SORTING VALUES

    return Response(
            { 
                'okay': True,
                'data': data_result, 
            }
        )
    
