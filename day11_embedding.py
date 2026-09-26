import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key=os.getenv("DASHSCOPE_API_KEY")

client=OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

text="苹果很好吃"

response=client.embeddings.create(
    model="text-embedding-v2",
    input=text
)

vector=response.data[0].embedding

print(f"文字：{text}")
print(f"向量长度：{len(vector)}")
print(f"前5个数字：{vector[:5]}")

import numpy as np

def get_embedding(text):
    res=client.embeddings.create(
        model="text-embedding-v2",
        input=text
    )

    return res.data[0].embedding

sentence_a="苹果很好吃"
sentence_b="香蕉很甜"
sentence_c="汽车跑得快"

vec_a=get_embedding(sentence_a)
vec_b=get_embedding(sentence_b)
vec_c=get_embedding(sentence_c)

def cosine_similarity(vec1,vec2):
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

sim_ab=cosine_similarity(vec_a,vec_b)
sim_ac=cosine_similarity(vec_a,vec_c)

print(f"【{sentence_a}】与【{sentence_b}】的相似度：{sim_ab:.4f}")
print(f"【{sentence_a}】与【{sentence_c}】的相似度：{sim_ac:.4f}")