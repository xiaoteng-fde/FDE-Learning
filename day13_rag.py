# 导入操作系统模块，用来读取环境变量
import os
# 导入 chromadb 向量数据库
import chromadb
# 从 dotenv 库导入加载环境变量的工具
from dotenv import load_dotenv
# 从 openai 库导入 OpenAI 客户端工具（用来调用百炼的Embedding和DeepSeek的大模型）
from openai import OpenAI

# 执行加载，把 .env 文件里的密钥读进系统环境变量
load_dotenv()

# 获取百炼的密钥（用于 Embedding）
dashscope_key = os.getenv("DASHSCOPE_API_KEY")
# 获取 DeepSeek 的密钥（用于最终生成）
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化百炼客户端（专门用来把文字变成向量）
# base_url 换成百炼的兼容地址
embed_client = OpenAI(
    api_key=dashscope_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 初始化 DeepSeek 客户端（专门用来最后生成回答）
llm_client = OpenAI(
    api_key=deepseek_key,
    base_url="https://api.deepseek.com"
)

# 导入 chromadb 底层的数据类型定义
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings


# class 定义类（面向对象编程的概念，这里你可以理解为：我们要造一个带包装盒的工具）
# 括号里的 EmbeddingFunction 意思是：继承官方规定的接口标准
class DashScopeEmbeddingFunction(EmbeddingFunction):
    # 在 class 里面，写在 def __call__ 的上面
    def __init__(self):
        # pass 意思是“占位/跳过”，代表这里暂时不需要额外处理
        pass
    # __call__ 这是一个魔术方法，意思是“当这个对象被调用时，执行什么”
    # input 输入参数
    # -> Embeddings 意思是：这是返回类型，返回一个向量列表
    def __call__(self, input: Documents) -> Embeddings:
        # 调百炼接口，把文本列表变成向量列表
        response = embed_client.embeddings.create(
            model="text-embedding-v2",
            input=input
        )
        return [data.embedding for data in response.data]

    # name 方法：ChromaDB 需要记录这个模型的名字
    def name(self):
        return "dashscope_embedding"
# 模拟企业文档切片（Chunking）
# 真实场景中，你需要用代码去读取 PDF 或 Word，然后按长度切分
chunks = [
    "员工报销流程：员工需要在费用发生后 30 天内，在系统中提交报销申请。",
    "报销所需材料：必须提供正规发票、支付凭证以及部门主管的签字确认。",
    "差旅费标准：一线城市住宿标准为每晚 500 元，二线城市为每晚 300 元。",
    "公司年假制度：入职满一年享有 5 天年假，满三年享有 10 天年假。",
    "报销审批时间：财务部通常在收到完整材料后的 7 个工作日内完成打款。"
]

# 给每个切片分配唯一的 ID
ids = [f"chunk_{i}" for i in range(len(chunks))]  # 列表推导式生成 chunk_0, chunk_1...

# 初始化 ChromaDB 客户端
# path 存到 "./chroma_rag_data" 文件夹下
chroma_client = chromadb.PersistentClient(path="./chroma_rag_data")

collection = chroma_client.get_or_create_collection(
    name="company_policy",
    # 注意这里加上括号：DashScopeEmbeddingFunction()
    embedding_function=DashScopeEmbeddingFunction()
)

# 将切片存入向量数据库
# 注意：因为我们传入了自定义的 embedding_function，Chroma 会自动调用它
collection.add(
    documents=chunks,
    ids=ids
)
print(f"✅ 成功存入 {len(chunks)} 条企业文档切片。")

# 模拟用户提问
user_question = "公司食堂好吃吗？"

# 第一步：检索（Retrieval）
# 去向量数据库里找最相关的 2 个切片
# n_results 意思是“返回结果的数量”
search_results = collection.query(
    query_texts=[user_question],
    n_results=2
)

# 提取检索到的文档内容
# search_results['documents'][0] 是一个列表，包含找出来的文档片段
retrieved_chunks = search_results['documents'][0]

# 把检索到的多个片段拼接成一段完整的上下文文本
# "\n".join() 意思是：用换行符把列表里的字符串连起来
context = "\n".join(retrieved_chunks)

# 打印检索到的内容，方便调试
print("\n🔍 检索到的相关上下文：")
print(context)

# 第二步：生成（Generation）
# 构造提示词，把用户问题和检索到的上下文拼在一起
# prompt 提示词
prompt = f"""
你是一个专业的企业客服助手。请根据以下参考资料，回答用户的问题。
如果参考资料中没有相关信息，请直接回答“抱歉，知识库中没有相关信息”，不要编造。

参考资料：
{context}

用户问题：{user_question}
"""

# 调用 DeepSeek 大模型生成最终回答
response = llm_client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # system 系统提示词，设定AI的角色和底线
        {"role": "system", "content": "你是一个严谨的企业客服，只根据提供的参考资料回答问题。"},
        # user 用户提示词，把拼接好的prompt发过去
        {"role": "user", "content": prompt}
    ]
)

# 获取并打印最终回答
final_answer = response.choices[0].message.content
print("\n🤖 AI 最终回答：")
print(final_answer)

