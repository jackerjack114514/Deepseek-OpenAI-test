import os
from openai import OpenAI
import pandas as pd
import numpy as np
import sympy as sp
import json

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")

field="材料力学"
question=f"按顺序生成一份{field}领域专有名词的中-日对译表，顺序依次为：中文-日文-假名注音"
prompt="要求内容详尽，结构明晰，尽可能多列举，保证内容准确无误"
messages0=[{'role':'user',
            'content':f"{question}\t{prompt}"}]

response=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages0,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)
msg_dict=response.choices[0].message.model_dump()
messages0.append(msg_dict)

output_dir="C:\\Users\\Administrator\\Desktop\\输入输出流\\数学专有名词表"
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,f'{field}名词表.txt')
with open(filepath,'w',encoding='utf-8') as f:
    for index,message in enumerate(messages0,1):
        m=message if isinstance(message,dict) else message.model_dump()
        f.write(f'====第{index}条对话=====\n')
        content=m.get('content') or ""
        f.write(f"{content}\n\n\n")

