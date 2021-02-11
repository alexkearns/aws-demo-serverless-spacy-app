import json
import os
import boto3
import logging

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        body = json.loads(record['body'])
        dynamodb = boto3.client('dynamodb')
        dynamodb.put_item(
            TableName=os.environ['DYNAMODB_TABLE'],
            Item={
                "HashedText": {
                    "S": body['hashed_key']
                },
                "Entities": {
                    "S": json.dumps(body['entities'])
                }
            }
        )
