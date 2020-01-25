from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse
from os import remove
from rest_framework.response import Response
from testbackend.aws_s3_credentials import s3_data
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from botocore.errorfactory import ClientError
from files.utils import S3Utils
import pandas as pd 
import logging

class ListUploadAndDeleteFile(APIView):

    def get(self, request):
        """
        Return list of files in s3
        """
        s3_client = S3Utils.get_s3_client()
    
        list_objs = s3_client.list_objects(Bucket=s3_data['bucket_name'])

        def get_only_key(obj):
            return obj['Key']

        list_only_keys = map(get_only_key, list_objs['Contents'])

        return Response({ 'okay': True, 'list': list_only_keys })

    def post(self, request):
        """
        Upload file to s3
        """
        s3_client = S3Utils.get_s3_client()

        file = request.FILES.get('file')

        if file:
            s3_client.upload_fileobj(
                file,  # File
                s3_data['bucket_name'],  # Name of bucket
                file.name #  Name of file in the bucket
            )

            return Response({ 'okay': True, 'file': file.name })
        
        return Response({ 'okay': False, 'error': 'File no puede ser nulo' })

    def delete(self, request, key_file):
        """
        Delete file with key_file parameter
        """
        s3_client = S3Utils.get_s3_client()

        s3_client.delete_object(Bucket=s3_data['bucket_name'], Key=key_file)

        return Response({ 'okay': True })


class DownloadFile(APIView):

    def get(self, request, key_file):
        """
        Download file from s3 with key_file
        """
        s3_client = S3Utils.get_s3_client()

        # Save file temporaly 
        try:
            S3Utils.download_file_s3(s3_key=key_file, local_path='./temp_files/temp.csv')
        except Exception as e:
            return Response({ 'okay': False, 'error': str(e) })

        # Read file to send on response
        with open('./temp_files/temp.csv', 'rb') as f:
            filedata = f.read()

        response = HttpResponse(filedata, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % (key_file)

        remove('./temp_files/temp.csv') # Delete file that will be send as response

        return response

class ProcessCsvData(APIView):

    def get(self, request, key_file):
        """
        Download file with key_file in s3 and read with pandas lib to show data in response.
        Filter columns with 'columns' parameter
        Sort filds with 'sort' and 'asc' parameter
        """
        # Save file temporaly 
        try:
            S3Utils.download_file_s3(s3_key=key_file, local_path='./temp_files/data_temp.csv')
        except Exception as e:
            return Response({ 'okay': False, 'error': str(e) })

        data = pd.read_csv("./temp_files/data_temp.csv")

        # [ INIT ] FILTER COLUMNS WITH PARAMS
        filter_columns = []
        # Columns that will be filters are in a string divided by ','
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

        # Get 'asc' query and check if number; if is > 0 the data is sort with ascending=true else ascending=false
        asc = request.query_params.get('asc')
        if asc:
            try:
                ascending = int(asc) > 0
            except Exception as e:
                return Response( { 'okay': False, 'error': 'El parametro \'asc\' debe ser entero' } )

        # Columns that will be sort are in a string divided by ','
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