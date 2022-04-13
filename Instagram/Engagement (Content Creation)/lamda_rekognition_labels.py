# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

import os, boto3, json
import urllib.parse
import urllib.request

REGION = "us-east-1"
MAX_LABELS = 20
MIN_CONFIDENCE = 75
client = boto3.client('rekognition')

def lambda_handler(event, context):
    print("Lambda using rekognition and s3")
    #print(event)
    
    # rekognition_client = boto3.client('rekognition', REGION)
    rekognition_client = boto3.client('rekognition', REGION)
    
    # 1) Use the below 2 lines for internal testing
    # s3_bucket = "scs-insta-urls"
    # s3_object = "urls.json"
    
    # 2) Use the below 2 lines for production
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_object = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("S3 Bucket: ", s3_bucket)
    print("S3 Object: ", s3_object)
    
    fileName = s3_object[s3_object.find('/') + 1 : ]
    print("File name (without folder): ", fileName)
    
    # parse json to get image URLS
    # s3 = boto3.resource('s3')
    # obj = s3.Object(s3_bucket, s3_object)
    # data = obj.get()['Body'].read().decode('utf-8')
    # json_data = json.loads(data)
    
    # result = []
    # for url in json_data:
    #     # print(sentence)
    #     response = client.detect_labels(Image={'S3Object':{'Bucket':s3_bucket,'Name': urllib.request.urlretrieve(url)}},
    #     MaxLabels=15)
    #     # print(response)
    #     result.append(print(response['Labels']))
    
    response = rekognition_client.detect_labels(
      Image = {
          "S3Object": {
            "Bucket": s3_bucket,
            "Name": s3_object,
          }
		},
		MaxLabels = MAX_LABELS,
		MinConfidence = MIN_CONFIDENCE
	)
	
	
	# This will log results of 'labels' part of the response to CloudWatch logs
    # print(result)
    print(response['Labels'])
    
    
    # Let's write 'labels' part of the response to S3 bucket
    # For input "justin1.jpg", the output file will be "justin1.jpg.json"
    # Verify in S3 bucket
    # s3_bucket = "scs-insta-urls"
    s3_resource = boto3.resource('s3', REGION)
    s3_output_object = s3_resource.Object(s3_bucket, 'output_label/' + fileName + ".json")
    s3_output_object.put(
        Body=(
            bytes(
                json.dumps(response['Labels']).encode('UTF-8')
            )
        )
    )
    
    return response['Labels']

