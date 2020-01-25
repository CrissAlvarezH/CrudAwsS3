from rest_framework.decorators import api_view
from rest_framework.response import Response
from testbackend.aws_s3_credentials import s3_data
import boto3
import pandas as pd 
import logging


def get_s3_client():
    sessionS3 = boto3.session.Session()

    s3Client = sessionS3.client(
            service_name='s3',
            region_name= s3_data['region_name'],
            aws_access_key_id= s3_data['aws_access_key_id'],
            aws_secret_access_key= s3_data['aws_secret_access_key']
        )

@api_view(['GET'])
def status(request):
    return Response({'okay': True})

@api_view(['GET'])
def load_data(request):
    data = pd.read_csv("./csv_data/test2.csv")

    # [ INIT ] FILTER COLUMNS WITH PARAMS
    filter_columns = ''

    query_columns = request.query_params.get('columns')
    if query_columns:
        filter_columns = query_columns.split(',')


    try:
        data_result = data if filter_columns == '' else data[filter_columns]
    except Exception as e:
        return Response( { 'okay': False, 'error': str(e)} )
    # [ END ] FILTER COLUMNS WITH PARAMS

    return Response(
            { 
                'okay': True,
                'data': data_result, 
            }
        )
    
