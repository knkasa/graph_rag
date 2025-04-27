# https://qiita.com/orc_jj/items/5d0858663fb663cd3f7d
# https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/NeptuneDatabaseKGIndexDemo/
# https://dev.classmethod.jp/articles/first-3steps-bedrock-claude-boto3/

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
