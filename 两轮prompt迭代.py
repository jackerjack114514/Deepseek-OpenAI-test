import os
from openai import OpenAI
import pandas as pd
import numpy as np
import sympy as sp
import json

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
#print("DEEPSEEK_API_KEY:","\t",os.environ.get("DEEPSEEK_API_KEY"))

question="提供当前考公考研的总体讯息"
prompt0="现基于上述要求，生成一版适用于DEEPSEEK API调用的提示词，要求内容详尽，且最终以markdown格式回复。"  #第一轮提示词
messages0=[{'role':'user',
            'content':f"{question}\n{prompt0}"}]

response0=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages0,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)

#====================================================================
msg_dict0=response0.choices[0].message.model_dump() #提示词迭代1
prompt1=response0.choices[0].message.content
messages0.append(msg_dict0)
print("第二轮提示词：",'\t',prompt1,'\n')

messages1=[{'role':'user',
            'content':f"{question}\n{prompt1}\n{question}"}]

response1=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages1,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)

msg_dict1=response1.choices[0].message.model_dump()
answer=response1.choices[0].message.content
messages0.append(msg_dict1)
print("第二轮回答：",'\t',answer,'\n')



output_dir='C:\\Users\\Administrator\\Desktop\\两轮迭代模型'
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,f"{question}.txt")
with open(filepath,'w',encoding="utf-8") as f:
    for index,message in enumerate(messages0,1):
        m=message if isinstance(message,dict) else message.model_dump()
        f.write(f'====第{index}条对话=====\n')
        f.write(json.dumps(m,ensure_ascii=False,indent=2))
        f.write("\n\n\n")


##须要修改！markdown格式回复但未保存为markdown格式

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




