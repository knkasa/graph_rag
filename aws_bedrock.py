# https://qiita.com/orc_jj/items/5d0858663fb663cd3f7d
# https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/NeptuneDatabaseKGIndexDemo/
# https://dev.classmethod.jp/articles/first-3steps-bedrock-claude-boto3/

import boto3
import json

# You'll need AmazonBedrockfullAccess permission for the IAM user.
session = boto3.Session(
        aws_access_key_id='xxxxx',
        aws_secret_access_key='yyyyyy',
        region_name='ap-northeast-1'
    ) 

client = session.client('bedrock-runtime', region_name='ap-northeast-1')


text = "こんにちは"

# Anthropic社のClaudeモデルのプロンプトフォーマットを参照： https://docs.anthropic.com/claude/docs/introduction-to-prompt-design#human--assistant-formatting
prompt = f"\n\nHuman: {text}\n\nAssistant:"

body = json.dumps(
        {
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        }
    )

resp = client.invoke_model(
        modelId="anthropic.claude-v2:1",  # you can lookup from clicking "Base models" in Bedrock webpage.
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    
#print(resp)
answer = resp["body"].read().decode()

#print(answer)
print(json.loads(answer)["completion"])


