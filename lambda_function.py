import json
import boto3
import io
import pandas as pd
s3_resourse = boto3.resource('s3') 
from io import StringIO
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
sns_arn = "arn:aws:sns:ap-south-1:590183859755:s3-arrival-notification"
trgt_bucket='doordash-target-zn-ashirbad'
def lambda_handler(event, context):
    print(event)
    key=event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    s3_client = boto3.client('s3')
    response=s3_client.get_object(Bucket=bucket,Key=key)
    file=response['Body'].read().decode('utf-8')
    print(file)
    df=pd.read_json(StringIO(file))
    a=df[df['status']=='delivered'].to_json(orient="records",date_format='iso')
    s3_client.put_object(Bucket=trgt_bucket,Key='transform.json',Body=a)
    # print(json_file1)
    # s3_client.put_object(Bucket=trgt_bucket,Key='json_file1')
    message=f"Input s3 file {key} has been processed successfully !!"
    resp_msg=sns_client.publish(Subject='Succes Daily Data Processing',TargetArn=sns_arn,Message=message,MessageStructure='text')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
