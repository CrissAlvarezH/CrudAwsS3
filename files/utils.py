import boto3
from testbackend.aws_s3_credentials import s3_data

class S3Utils():

    @staticmethod
    def get_s3_client():
        return boto3.client(
                service_name='s3',
                region_name= s3_data['region_name'],
                aws_access_key_id= s3_data['aws_access_key_id'],
                aws_secret_access_key= s3_data['aws_secret_access_key']
            )

    @staticmethod
    def download_file_s3(s3_key, local_path):
        s3_client = S3Utils.get_s3_client()

        with open(local_path, 'wb') as file:
            try:
                s3_client.download_fileobj(s3_data['bucket_name'], s3_key, file)
            except ClientError:
                raise Exception('%s no existe en el bucket' % (s3_key))