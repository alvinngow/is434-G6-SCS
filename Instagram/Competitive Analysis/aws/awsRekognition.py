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
import timeit

REGION = "us-east-1"
MIN_CONFIDENCE = 75
client = boto3.client('rekognition')

def lambda_handler(event, context):
    start = timeit.default_timer()
    stop = 0
    print("Lambda using rekognition and s3")

    rekognition_client = boto3.client('rekognition', REGION)
    
    s3_bucket = "shurui-image-text"
    s3_object = "uploads/postImage_" #0.jpg
    
    result = []
    num = 1045
    while ((stop - start < 780) and num < 1481):
        objName = s3_object + str(num) + ".jpg"
    
        response = rekognition_client.detect_text(
          Image = {
              "S3Object": {
                "Bucket": s3_bucket,
                "Name": objName,
                  }
            }
        )
        result.append(response['TextDetections'])
        num += 1
        stop = timeit.default_timer()

    print(num)
    s3_resource = boto3.resource('s3', REGION)
    s3_output_object = s3_resource.Object(s3_bucket, "output_text/" + str(num) + ".json")
    s3_output_object.put(
        Body=(
            bytes(
                json.dumps(result, indent=4).encode('UTF-8')
            )
        )
    )
    return num