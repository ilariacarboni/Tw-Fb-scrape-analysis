import boto3
import csv
import json
from s3_client import s3
from datetime import datetime

bucket_name = 'ilaria-bucket'

def save_to_s3(json_obj, key_name):
    json_str = json.dumps(json_obj)
    json_bytes = json_str.encode('utf-8')
    s3.put_object(Bucket=bucket_name, Key=key_name, Body=json_bytes)

def retrieve_from_s3():
    objects = s3.list_objects_v2(Bucket=bucket_name)
    '''
    specific_date = datetime.datetime(2023, 3, 1)  
    formatted_date = specific_date.strftime('%Y-%m-%d')
    '''
    specific_date = datetime.now().strftime('%Y-%m-%d')
    filtered_objects = []
    for obj in objects['Contents']:
        if obj['LastModified'].strftime('%Y-%m-%d') == specific_date:
            key_name = obj['Key']
            obj = s3.get_object(Bucket=bucket_name, Key=key_name)
            json_bytes = obj['Body'].read()
            json_str = json_bytes.decode('utf-8')
            json_obj = json.loads(json_str)
            filtered_objects.append(json_obj)
    return filtered_objects
