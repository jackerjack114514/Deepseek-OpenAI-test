import os
from openai import OpenAI
import pandas as pd
import numpy as np
import sympy as sp
import json

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
#print("DEEPSEEK_API_KEY:","\t",os.environ.get("DEEPSEEK_API_KEY"))



question0="日本にはこんなことわざがある。「十で神童、十五で才子、二十過ぎれば只の人」実際、そういう子供たちはいつまでも私たちの周りにたくさんいる。神童がそのまま神人になったのではたまらないが、そこはよくしたもので、ほとんどの神童は、やがて「只の凡児」になっていくのである。だからこそ、社会平和を保っているにちがいない。そしてここに私は日本人の正直な価値観を見る。日本人はけっして天才を歓迎しない。ずば抜けた才を持った人は、たしかに貴重な存在ではあるが、彼らは往々して常識を欠け、性格的にも偏っており、協調性に乏しい。日本人はそうした人物を尊敬しはするが、決して親しみは持たないのである。それよりも凡人こそが好ましく、だからこそ「只の凡児」は人気を博し、大学の教師でありながら、けっこう下世話に通じた俗人である「唯野教授」を笑いながら歓迎するのだ。"
prompt0="###将上述文章翻译成日文,仅返回译文本身。"     #prompt为const
messages0=[{'role':'user',
            'content':f"{question0}\n{prompt0}"}]
record=messages0

question1=""
prompt1="###将上述文章翻译成中文,仅返回译文本身。"

for i in range(50):
    response0=client.chat.completions.create(           #中-日
        model='deepseek-flash',
        messages=messages0,
        reasoning_effort='high',
        extra_body={'thinking':{'type':'enabled'}}
    )
    msg_dict0=response0.choices[0].message.model_dump() 
    question1=response0.choices[0].message.content
    record.append(msg_dict0)

    #print("第二轮提示词：",'\t',prompt1,'\n') 
    messages1=[{'role':'user',                          #日-中
            'content':f"{question1}\t{prompt1}"}]
    response1=client.chat.completions.create(
        model='deepseek-flash',
        messages=messages1,
        reasoning_effort='high',
        extra_body={'thinking':{'type':'enabled'}}
    )
    msg_dict1=response1.choices[0].message.model_dump()
    question0=response1.choices[0].message.content
    record.append(msg_dict1)
    #print("第二轮回答：",'\t',answer,'\n')



output_dir='C:\\Users\\Administrator\\Desktop\\翻译100次'
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,"deepseek翻译100次-2.txt")
with open(filepath,'w',encoding="utf-8") as f:
    for index,message in enumerate(record,1):
        m=message if isinstance(message,dict) else message.model_dump()
        f.write(f'====第{index}条对话=====\n')
        #f.write(json.dumps(m,ensure_ascii=False,indent=2))
        #f.write("\n\n\n")
        content=m.get("content") or ""
        f.write(f"{content}\n\n\n")






