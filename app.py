import os
import json
import boto3
from datetime import datetime,timedelta
import pytz
from boto3.session import Session
import requests

aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key=os.environ['aws_secret_access_key']
region_name = os.environ ['region_name']
bucket_name = os.environ ['bucket_name']
slack_url = os.environ ['slack_url']

def slack_msg(bucket_name,s3_file):
    S3_url = "https://s3"+region_name+".amazonaws.com/"+bucket_name+"/"+s3_file
    url = slack_url
    du_url = s3_file.split("/")[0]
    header = {"Content-type": "application/json"}
    payload = {
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "\n\n*New file has been uploaded to S3*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*DU-URL:* "+du_url+"\n"+ "*S3_Bucket:* "+bucket_name +"\n *File_Name:* "+s3_file+" \n *URL: *"+S3_url
			},
		},
	]
}
    requests.post(url,headers=header,json=payload )

if __name__ == '__main__':
    
    session = Session(aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource('s3',region_name=region_name)
    your_bucket = s3.Bucket(bucket_name)
    time_now_UTC = datetime.utcnow().replace(tzinfo=pytz.UTC)
    delta_hours = time_now_UTC - timedelta(hours=2)
    for s3_file in your_bucket.objects.all():
    #print(s3_file.last_modified)
        if s3_file.last_modified >= delta_hours:
            print("New logs files are uploaded to: "+bucket_name+" File name is: " +str(s3_file.key))
            slack_msg(bucket_name,s3_file.key)
