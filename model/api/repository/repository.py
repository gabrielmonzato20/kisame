# repository.py
import pickle
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
class Repository:
    def __init__(self):
        print(os.getenv('LOCALSTACK_ENDPOINT_URL'))
        self.s3 =  boto3.client("s3", endpoint_url=os.getenv('LOCALSTACK_ENDPOINT_URL'))
        self.dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv('LOCALSTACK_ENDPOINT_URL'))

    def load_known_faces(self,filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data['encodings'], data['labels']

    def save_video_to_s3(self,data, unique_key):
        
        self.s3.upload_fileobj(data, os.getenv('S3_BUCKET_NAME'), f'{unique_key}.mp4')

    def get_criminal_records(self,id):
        table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))
        response = table.get_item(Key={'id': id})
        item = response.get('Item', None)

        if item:
            return item
        else:
            return None