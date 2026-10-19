import os
from openai import OpenAI

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
#print(repr(os.environ.get("DEEPSEEK_API_KEY")))

'''
response=client.chat.completions.create(
    model='deepseek-chat',
    messages=[{"role":"user",
               "content":"为我生成一份线性代数领域的中文-日文-英文专有名词对照列表"}])

print(response.choices[0].message.content)
'''

#WARNING！消息列表messages必须严格按照对话实际发生的顺序排列！
#system-user-assistant-tool-assistant最终回答

messages1=[{'role':'user',
            'content':'比较9.11和9.8的大小'}]  #待维护的messages列表

response1=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages1,
    reasoning_effort='high',      #low/medium/high
    extra_body={"thinking":{"type":"enabled"}} #enabled: open thinking mod
)

messages1.append(response1.choices[0].message.model_dump())  #必须转换为Python字典型，否则i['role']遍历时报错

msg_dict=response1.choices[0].message.model_dump()

for i in messages1:
    #print(f"[{i['role']}]:{i['content']}")   #f:格式化字符串
    print(i.keys())  #词典所含标签
    print(i)         #输出整本词典



#另：两种包括思考过程与最终回答的思考模式
'''
print(response1.choices[0].message.content)
print("\n思考过程：", getattr(response1.choices[0].message, "reasoning_content", None))
print("\n最终回答：", response1.choices[0].message.content)
'''
'''
reasoning1=response1.choices[0].message.reasoning_content
answer1=response1.choices[0].message.content
print("思考过程:",reasoning1,'\n\n',"最终回答：",answer1)
'''