import os
from openai import OpenAI
import pandas as pd
import numpy as np
import sympy as sp
import json

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
#print("DEEPSEEK_API_KEY:","\t",os.environ.get("DEEPSEEK_API_KEY"))

question="判断目前日元汇率走势。"
prompt0="现基于上述要求，生成一版适用于DEEPSEEK API调用的提示词，要求内容详尽。"
messages0=[{'role':'user',
            'content':f"{question}\n{prompt0}"}]

response0=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages0,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)

#====================================================================
prompt1=response0.choices[0].message.model_dump() #提示词迭代1

print("第二轮提示词：",'\t',prompt1,'\n')

messages1=[{'role':'user',
            'content':f"{question}\n{prompt1}\n{question}"}]

response1=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages1,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)

msg_dict=response1.choices[0].message.model_dump()
answer=response1.choices[0].message.content
print("第二轮回答：",'\t',answer,'\n')




'''
#messages1=[{"role":"system","content":""},   #角色提示词
#           {"role":"user","content":""}]     #问询内容

response1=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)

messages1.append(response1.choices[0].message.model_dump())
msg_dict=response1.choices[0].message.model_dump()

for i in messages1:
    print(i.keys())
    print(i)
'''




