import os
import requests
from openai import OpenAI
import time
import numpy as np
import pandas as pd

#或可令模型自行生成关键词，主动调用search接口查询相关信息，以便迭代回答

client=OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url='https://api.deepseek.com')
api_key=os.environ.get('DEEPSEEK_API_KEY')

KEY_WORD='日本 研究生 套磁 难度'   #网页fetch关键词

response0=requests.post(
    'https://api.deepseek.com/v1/tools/search',
    headers={
        'Authorization':f'Bearer {os.environ.get('DEEPSEEK_API_KEY')}',
        'content-Type':'application/json'
    },
    json={
        'query': f'{KEY_WORD}\t中文',   #KEY WORD
        'count':50,            #结果返回数，1-50
        'need_content':True    #返回网页正文
    },
    timeout=100
)


#print(response0.json()['results'],'\n\n')

for index,result in enumerate(response0.json()['results']):   #按顺序输出搜索结果
    print(result['title'],result['url'])
    print('\n')
    print(result['summary'])
    print('\n')
    print(result['content'])
    print(f'=============第{index}条结果=============\n\n')
print('####################################\n\n\n')

response0.raise_for_status()

results=response0.json()['results']

content_get=[]
for i,r in enumerate(results,start=1):
    part=(
        f"[{i}] title:{r.get('title','无')}\n"
        f"URL: {r.get('url','无')}\n"
        f"摘要: {r.get('summary','无')}\n"
        f"正文: {r.get('content','无')}\n"
    )
    content_get.append(part)

content_text='\n'.join(content_get)     #总返回search结果列表


message1=[{"role": "user",
           "content": f"从以下搜素结果中整理出有用的信息，告诉我{KEY_WORD}的相关信息：\n============\n{content_text}\n============\n"}]


response=client.chat.completions.create(
    model='deepseek-flash',
    messages=message1,
    reasoning_effort='max',
    extra_body={'thinking':{'type':'enabled'}},
    logprobs=True,
    top_logprobs=5
)

msg_dict=response.choices[0].message.model_dump()
print(response.choices[0].message.content)
message1.append(msg_dict)

output_dir='D:\\输入输出流\\网页抓取接口测试'   #当前环境无权限写入administrator文件夹
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,f'\'{KEY_WORD}\' 搜索结果.txt')
with open(filepath,'w',encoding='utf-8') as f:
    for index,message in enumerate(message1,1):
        m=message if isinstance(message,dict) else message.model_dump()
        f.write(f'=========第{index}条对话========\n')
        content=m.get('content') or ''
        f.write(f'{content}\n\n\n')

