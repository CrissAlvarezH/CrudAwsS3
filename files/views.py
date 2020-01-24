from rest_framework.decorators import api_view
from rest_framework.response import Response
from testbackend.aws_s3_credentials.py import s3_data
import boto3

sessionS3 = boto3.session.Session()

def get_s3_client():
    s3Client = sessionS3.client(
            service_name='s3',
            region_name= s3_data['region_name'],
            aws_access_key_id= s3_data['aws_access_key_id'],
            aws_secret_access_key= s3_data['aws_secret_access_key']
        )

@api_view(['GET'])
def status(request):
    return Response({'okay': True})
