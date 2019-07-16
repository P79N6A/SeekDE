import os
import re
import boto3
from botocore.exceptions import ClientError

if not 'KAGGLE_CONFIG_DIR' in os.environ.keys():
    os.environ['KAGGLE_CONFIG_DIR'] = os.getcwd()

import kaggle

def download_dataset(url, dest, unzip=True):
    try:
        dataset = re.search(r'kaggle.com/([^/]+)/([^/]+)', url).group()
        if not 'kaggle.com/' in dataset:
            raise ValueError
        else:
            dataset = dataset.replace('kaggle.com/', '')
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(dataset, path=dest, unzip=unzip)
    except (AttributeError, ValueError):
        print('Check your url: {}'.format(url))
        exit()

class S3Client(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.client = boto3.client('s3',
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)
        self.__buckets = [row['Name'] for row in self.client.list_buckets()['Buckets']]

    def upload_file(self, bucket, src, dest):
        try:
            assert bucket in self.__buckets, 'Bucket %s not found!' % bucket
            response = self.client.upload_file(src, bucket, dest)
        except (AssertionError, ClientError) as msg:
            print(msg)
            return False
        else:
            return True

