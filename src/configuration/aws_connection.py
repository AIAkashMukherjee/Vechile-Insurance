import boto3
import os
from src.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME


class S3Client:

    s3_client=None
    s3_resource = None
    def __init__(self, region_name=REGION_NAME):

        if S3Client.s3_resource==None or S3Client.s3_client==None:
            
            if AWS_ACCESS_KEY_ID_ENV_KEY is None:
                raise Exception(f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not not set.")
            if AWS_SECRET_ACCESS_KEY_ENV_KEY is None:
                raise Exception(f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set.")
        
            S3Client.s3_resource = boto3.resource('s3',
                                            aws_access_key_id=AWS_ACCESS_KEY_ID_ENV_KEY,
                                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ENV_KEY,
                                            region_name=region_name
                                            )
            S3Client.s3_client = boto3.client('s3',
                                        aws_access_key_id=AWS_ACCESS_KEY_ID_ENV_KEY,
                                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ENV_KEY,
                                        region_name=region_name
                                        )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client