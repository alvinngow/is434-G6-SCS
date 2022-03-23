# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }
import os, boto3, json
import urllib.parse

REGION = "us-east-1"
client = boto3.client('comprehend')

def lambda_handler(event, context):
    print("Lambda using comprehend and s3")
    #print(event)
    
    # rekognition_client = boto3.client('rekognition', REGION)
    client = boto3.client('comprehend', REGION)
    
    # 1) Use the below 2 lines for internal testing
    # s3_bucket = "is434-shao"
    # s3_object = "test.json"
    
    # 2) Use the below 2 lines for production
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_object = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("S3 Bucket: ", s3_bucket)
    print("S3 Object: ", s3_object)
    
    # parse json
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket, s3_object)
    data = obj.get()['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    
    result = []
    for sentence in json_data:
        # print(sentence)
        response = client.detect_sentiment(Text=sentence,LanguageCode='en')
        # print(response)
        result.append(response)
    
	
	# This will log 'labels' part of the response to CloudWatch logs
    print(result)
    
    # Let's write 'labels' part of the response to S3 bucket
    # For input "justin1.jpg", the output file will be "justin1.jpg.json"
    # Verify in S3 bucket
    s3_bucket = "is434-shao-output"
    s3_resource = boto3.resource('s3', REGION)
    s3_output_object = s3_resource.Object(s3_bucket, s3_object + ".json")
    s3_output_object.put(
        Body=(
            bytes(
                json.dumps(result).encode('UTF-8')
            )
        )
    )
    
    return result