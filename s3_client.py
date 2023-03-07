import configparser
import boto3

config = configparser.RawConfigParser()
config.read('config.ini')
access_key = config['amazon']['ACCESS_KEY']
secret_access_key = config['amazon']['SECRECT_KEY']
s3 = boto3.client('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key)