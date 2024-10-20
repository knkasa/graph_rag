# https://qiita.com/orc_jj/items/5d0858663fb663cd3f7d
# https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/NeptuneDatabaseKGIndexDemo/
# https://dev.classmethod.jp/articles/first-3steps-bedrock-claude-boto3/

#pip install llama-index-llms-bedrock
#pip install llama-index-graph-stores-neptune
#pip install llama-index-embeddings-bedrock
# pip install -U llama-index-readers-file

import boto3
import json
import wikipedia
import os

from llama_index.graph_stores.neptune import NeptuneAnalyticsGraphStore
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.llms.bedrock import Bedrock
from llama_index.embeddings.bedrock import BedrockEmbedding
from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader,
    KnowledgeGraphIndex,
    Settings,
    )

os.chdir('C:/Users/knkas/Desktop/GraphRag')
graph_identifier = "g-8kl0q0kgs8"  # for Neptune graph.

# You'll need AmazonBedrockfullAccess & NeptuneFullAccess permission for the IAM user.
session = boto3.Session(
        aws_access_key_id='xxxxxx',
        aws_secret_access_key='yyyyyy',
        region_name='ap-northeast-1'
    )

llm = Bedrock(model="anthropic.claude-v2:1")
embed_model = BedrockEmbedding(model="amazon.titan-embed-text-v1")

Settings.llm = llm
Settings.embed_model = embed_model
Settings.chunk_size = 512

# Read data from this directory.
if not os.path.exists('./data'):
    os.makedirs('data')
documents = SimpleDirectoryReader(input_dir="./data").load_data()


'''
# Go to AWS and create NeptuneAnalytics.  Allow internet & private VPC with security group & subnet.
graph_store = NeptuneAnalyticsGraphStore(graph_identifier=graph_identifier)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# そこそこ時間かかる
index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    )

# save database information for faster access later.
index.storage_context.persist("./persist")
query_engine = index.as_query_engine(include_text=False, response_mode="tree_summarize") # include_text=True will return the rag data.
response = query_engine.query("悟空がカメハウスで共に暮らしていたのは誰？")
print(response.response)
print(response.source_nodes) # it will return if include_text=True.
'''


# Once data is saved, you can run below to read the saved data.
graph_store = NeptuneAnalyticsGraphStore(graph_identifier=graph_identifier)
storage_context = StorageContext.from_defaults(
    graph_store=graph_store,
    persist_dir="./persist"
    )

load_index = load_index_from_storage(storage_context=storage_context)
query_engine = load_index.as_query_engine(include_text=False, response_mode="tree_summarize") # include_text=True will return the rag data.
response = query_engine.query("悟空がカメハウスで共に暮らしていたのは誰？")
print(response.response)
print(response.source_nodes) # it will return python list if include_text=True.

breakpoint()

'''
# If you want to append new data, run below.
new_documents = SimpleDirectoryReader(input_dir="./data").load_data()
load_index.refresh_ref_docs(
    documents=new_documents,
    storage_context=storage_context,
    )
load_index.storage_context.persist("./persist")
query_engine = load_index.as_query_engine(include_text=False, response_mode="tree_summarize") # include_text=True will return the rag data.
response = query_engine.query("悟空がカメハウスで共に暮らしていたのは誰？")
print(response.response)
print(response.source_nodes) # it will return if include_text=True.
'''

