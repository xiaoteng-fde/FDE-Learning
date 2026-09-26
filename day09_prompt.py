import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
api_key=os.getenv("DEEPSEEK_API_KEY")
client=OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
import json
response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"system","content":"你是一个信息提取助手。请从用户提供的文本中提取姓名、年龄、职业。必须严格输出JSON格式"
"包含name，age，occupation三个字段。不要输出任何多余的文字。"},
        {"role":"user","content":"我叫张伟，今年35岁，目前在深圳做产品经理，工作了十年。"}
    ],
    response_format={"type":"json_object"}
)
raw_content=response.choices[0].message.content
print("AI 原始输出：")
print(raw_content)
parsed_data=json.loads(raw_content)
print("\n解析后的Python字典：")
print(parsed_data)
print(f"\n提取出的姓名是：{parsed_data['name']}")
print(f"提取出的年龄是：{parsed_data['age']}")