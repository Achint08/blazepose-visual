import json
import boto3


def get_all_data(event, context):
    """Handler function to get all data from dynamodb and return to API

    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('blazepose-visualization')
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    for d in data:
        d['description'] = d['description'].replace('\\n', "\n")

    response = {"statusCode": 200, "body": json.dumps(data)}

    return response
