import json
from openai import OpenAI

client = OpenAI(api_key="<你的Key>", base_url="https://api.deepseek.com")

# 定义工具（以查天气为例）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名"}
                },
                "required": ["location"]
            }
        }
    }
]

# 1. 初始化消息列表：system + user
messages = [
    {"role": "system", "content": "你是一个乐于助人的天气助手。"},
    {"role": "user", "content": "杭州天气怎么样？"}
]

# 2. 第一次调用：模型可能返回 tool_calls
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    tools=tools
)
assistant_msg = response.choices[0].message

# 3. 把 assistant 的回复（含 tool_calls）追加到历史
messages.append(assistant_msg)

# 4. 如果模型发起了工具调用，执行并追加 tool 消息
if assistant_msg.tool_calls:
    for tool_call in assistant_msg.tool_calls:
        # 模拟执行工具（实际中应调用你的函数）
        tool_result = "24℃ 晴"
        
        # 追加 tool 消息，必须带上 tool_call_id
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        })

# 5. 第二次调用：带着 tool 结果让模型生成最终回答
final_response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    tools=tools
)

# 6. 追加最终的 assistant 回复
messages.append(final_response.choices[0].message)

# 7. 打印完整对话历史（包含所有角色）
for msg in messages:
    role = msg["role"] if isinstance(msg, dict) else msg.role
    content = msg.get("content") if isinstance(msg, dict) else msg.content
    print(f"[{role}]: {content}")

