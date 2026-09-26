# 导入 chromadb 库
import chromadb

# 初始化一个本地数据库客户端
# Client 客户端（代表你连接数据库的通道）
# Settings 设置
# is_persistent 意思是“是否持久化”。True 代表数据存到硬盘上，关了电脑也不会丢
# path 路径，数据存到当前目录下的 "chroma_data" 文件夹里
client = chromadb.PersistentClient(path="./chroma_data")

# 创建一个名为 "fde_knowledge" 的集合
# get_or_create_collection 意思是：如果这个集合存在就获取它，不存在就创建它
collection = client.get_or_create_collection(name="fde_knowledge")

# 打印测试
print("向量数据库初始化成功！集合名称：", collection.name)

# 准备 4 条文本数据（模拟企业的知识库文档）
documents = [
    "红富士苹果又脆又甜，产自山东烟台。",
    "海南香蕉含有丰富的钾元素，口感软糯。",
    "特斯拉Model 3 百公里加速仅需 3.3 秒。",
    "大众帕萨特是一款经典的商务轿车，空间宽敞。"
]

# 准备 4 个对应的 ID（就像数据库里的主键，必须是唯一的字符串）
ids = ["doc1", "doc2", "doc3", "doc4"]

# 把文档和 ID 添加到集合中
# add 添加
# documents 文档列表
# ids 标识符列表
collection.add(
    documents=documents,
    ids=ids
)

print(f"\n成功存入 {len(documents)} 条文档到向量数据库。")

# 准备一个用户提问
query_text = "有什么好吃的水果推荐吗？"

# 执行查询
# query 查询
# query_texts 查询文本列表（可以同时问多个问题）
# n_results 返回结果的数量（这里设置为2，也就是找最相似的2条）
results = collection.query(
    query_texts=[query_text],
    n_results=2
)

# 打印查询结果
print(f"\n用户提问：{query_text}")
print("-" * 30)

# results['documents'] 是一个二维列表，取第一个结果列表
# [0] 代表第一个问题的返回结果
# 逐个打印出来
for i, doc in enumerate(results['documents'][0]):
    # i+1 代表序号，从1开始
    # doc 是文档内容
    print(f"匹配结果 {i+1}：{doc}")

