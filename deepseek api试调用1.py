import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

print(repr(os.environ.get('DEEPSEEK_API_KEY')))

response = client.chat.completions.create(
    model="deepseek-chat",  # 或 deepseek-reasoner
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
