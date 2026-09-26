# 导入操作系统模块，用来读取环境变量
import os
# 导入 JSON 模块，用来处理 AI 返回的工具参数
import json
# 从 dotenv 库导入加载环境变量的工具
from dotenv import load_dotenv
# 从 openai 库导入 OpenAI 客户端工具
from openai import OpenAI

# 执行加载，把 .env 文件里的密钥读进系统环境变量
load_dotenv()
# 获取密钥，赋给变量 api_key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# def 定义函数（define）
# get_weather 函数名（获取天气）
# city 参数名（城市）
# 返回（return）一段模拟的天气数据
def get_weather(city):
    # 这里我们模拟一个本地数据库或API的返回
    return f"{city}今天是晴天，气温25摄氏度，微风。"

# 打印测试一下函数能不能跑
# print 打印 / get_weather 调用函数 / "北京" 传入的参数
print("本地函数测试：", get_weather("北京"))

# tools 工具列表（这是一个数组，可以放多个工具）
# 这里我们定义了一个名为 get_weather 的工具
tools = [
    {
        # type 类型：这里是 function（函数）
        "type": "function",
        # function 函数的具体定义
        "function": {
            # name 函数名：必须和你的 Python 函数名一模一样
            "name": "get_weather",
            # description 描述：告诉大模型这个工具是干嘛用的，描述越清楚，AI 调用越准
            "description": "获取指定城市的实时天气",
            # parameters 参数（说明这个函数需要什么输入）
            "parameters": {
                # type 类型：参数是一个对象（object）
                "type": "object",
                # properties 属性（具体包含哪些参数）
                "properties": {
                    # city 参数名
                    "city": {
                        # type 类型：城市名是字符串（string）
                        "type": "string",
                        # description 描述：告诉 AI 传入什么格式的城市名
                        "description": "城市名称，例如：北京、上海"
                    }
                },
                # required 必须的（告诉 AI 哪些参数是必填的）
                "required": ["city"]
            }
        }
    }
]

# 发起请求
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        # user 用户提问
        {"role": "user", "content": "帮我查一下北京现在的天气怎么样？"}
    ],
    # tools 把刚才写的工具说明书传给大模型
    tools=tools
)

# 获取 AI 的第一轮回复
# message 消息对象
first_message = response.choices[0].message

# 打印看看 AI 是否决定调用工具
print("AI 的第一轮回复：")
print(first_message)

# 检查 AI 是否决定调用工具（tool_calls 是否存在且不为空）
if first_message.tool_calls:
    # 获取第一个工具调用（可能有多个，我们取第一个）
    tool_call = first_message.tool_calls[0]

    # 获取工具名（也就是函数名）
    function_name = tool_call.function.name

    # 获取 AI 传过来的参数（注意：它是字符串格式的 JSON）
    # json.loads 把 JSON 字符串解析成 Python 字典
    function_args = json.loads(tool_call.function.arguments)

    # 从字典里取出 city 参数
    city = function_args["city"]

    # 打印调试信息
    print(f"\nAI 决定调用函数：{function_name}，参数为：{city}")

    # 执行我们本地的函数，拿到天气结果
    # 假设函数名是 get_weather，我们这里写个简单的判断
    if function_name == "get_weather":
        weather_result = get_weather(city)
        print(f"本地函数执行结果：{weather_result}")

        # 准备第二轮请求，把 AI 的第一次回复和工具结果一起塞回去
        # role 角色：tool 工具
        # tool_call_id 工具调用ID：告诉 AI 这是针对哪个请求的回答
        # content 内容：工具的返回结果
        second_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                # 用户原始问题
                {"role": "user", "content": "帮我查一下北京现在的天气怎么样？"},
                # AI 刚才决定调用工具的回复（必须带上，维持对话状态）
                first_message,
                # 工具执行的结果
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": weather_result
                }
            ]
        )

        # 打印 AI 最终整理好的自然语言回复
        print("\nAI 最终的回复：")
        print(second_response.choices[0].message.content)
