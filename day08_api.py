# os 是 operating system（操作系统）的缩写，用来读取操作系统的环境变量
import os

# from 从……里面，dotenv 库，import 导入 load_dotenv（加载环境变量）的功能
from dotenv import load_dotenv

# 从 openai 库里导入 OpenAI 工具模板
from openai import OpenAI

# 执行加载动作：把 .env 文件里的内容，读进操作系统的环境变量里
load_dotenv()

# os.getenv 意思是：从环境变量里“获取（get）”名字叫 "DEEPSEEK_API_KEY" 的值
# 把这个值赋给 api_key 变量
api_key = os.getenv("DEEPSEEK_API_KEY")

# 接下来初始化客户端
# 这里的 api_key 直接写变量名，不再写真实的密钥
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
# （下面继续写你的 messages 和 print 代码即可）

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"system","content":"你是一个乐于助人的FDE助理"},
        {"role":"user","content":"请用一句话向我问好，并告诉我什么是FDE"}
    ]
)

print(response.choices[0].message.content)