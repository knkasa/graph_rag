# https://qiita.com/orc_jj/items/5d0858663fb663cd3f7d
# https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/NeptuneDatabaseKGIndexDemo/
# https://dev.classmethod.jp/articles/first-3steps-bedrock-claude-boto3/

# When you setup Kendra for RAG, you will create a new role or choose existing role that has Kendra access policy, but you also need BatchPutDocument.
# You do not have this policy, so will need to create one.
# Go to IAM, click policy, click "create policy".
# Choose Kendra for service.  Under "Write" choose "BatchPutDocument".  
# For the resouce, specify ARN "arn:aws:kendra:us-east-1:<your account number>:index/<your kendra index like 1e6c2e5a>". 
# Name you policy.  Attach this policy to your kendra role.

# When uploading files to s3, attach the metadata info like s3_document_id=doc001, author=xxx, category=ccc and etc.  
# When synchronizing s3 with Kendra, under s3 field mapping, add these s3_document_id, author, category under s3_field_name, and insert authour, category under index_field_name column.
# Finally, when you query, you can filter by authour, category, a3_document_id.  

import boto3
import json

# You'll need AmazonBedrockfullAccess policy for the IAM user.
session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        #region_name='ap-northeast-1'
    ) 

bedrock_client = session.client('bedrock-runtime', region_name='us-east-1')

system_prompt = "日本語はわかりますか？"

payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "temperature": 0.5,
            "max_tokens": 5000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        }
                    ]
                }
            ]
        }

response_raw = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json",
    )

response = json.loads(response_raw['body'].read())['content'][0]['text']
print(response)
