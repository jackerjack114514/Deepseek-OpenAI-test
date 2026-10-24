import os
from openai import OpenAI
import pandas as pd
import numpy as np
import sympy as sp
import json

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
#print("DEEPSEEK_API_KEY:","\t",os.environ.get("DEEPSEEK_API_KEY"))

question0='言葉によるイメージの相違は翻訳の上で基本的に避けられない問題で、この相違を極力最小限食い止める努力をする以外に方法はないと、西山千氏はドナルド・キーン氏の話を紹介する。キーン氏が日本の小説を英訳していたら、和服の女主人公が新しい白足袋をはいて訪問先へ出かけたというくだりになった。英語では「足袋」は通用しない。脚注で足袋を説明をするのも教科書みたいだ。また、仮にこれを「白い靴下」としたら、この女性はテニスをやりに出かけるのかといわれるだろう。考えたすえ、「白い手袋をはめて出かけた」と訳したという。西洋では、正式訪問などの場合は女性は白い手袋をはめるのである。和服なら白い足袋、洋装なら白い手袋という習慣の相違を見事に克服して、小説の文章の流れを妨げずに英国民の読者に女主人公の行動の意味を伝えたのであった。ただし、「足袋」を「たび」と読めないため「足」を「手」に間違えたのではないかと、日本人の英語先生あたりから投書が来るのではないかという心配もあったそうだ。出かけるのかといわれるだろう。考えたすえ、「白い手袋をはめて出かけた」と訳したという。西洋では、正式訪問などの場合は女性は白い手袋をはめるのである。和服なら白い足袋、洋装なら白い手袋という習慣の相違を見事に克服して、小説の文章の流れを妨げずに英国民の読者に女主人公の行動の意味を伝えたのであった。ただし、「足袋」を「たび」と読めないため「足」を「手」に間違えたのではないかと、日本人の英語先生あたりから投書が来るのではないかという心配もあったそうだ。'
prompt0="###将上述文章翻译成地道的中文，仅返回译文本身。" 
messages0=[{'role':'user',
            'content':f"{question0}\n{prompt0}"}]
record=messages0

response=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages0,
    reasoning_effort='high',
    extra_body={'thinking':{'type':'enabled'}}
)
msg_dict=response.choices[0].message.model_dump()
question1=response.choices[0].message.content     #译文
record.append(msg_dict)

prompt1="###参考原文，对上述译文进行修改校对，仅返回校对后的译文本身。"

for i in range(20):
    messages1=[{'role':'user',                   
            'content':f"{question1}\t{prompt1}"}]
    response1=client.chat.completions.create(
        model='deepseek-flash',
        messages=messages1,
        reasoning_effort='high',
        extra_body={'thinking':{'type':'enabled'}}
    )
    msg_dict1=response1.choices[0].message.model_dump()
    question1=response1.choices[0].message.content    #更新译文
    record.append(msg_dict1)

output_dir="C:\\Users\\Administrator\\Desktop\\输入输出流\\多轮校对"
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,f"译文校对-{question0[:5]}.txt")
with open(filepath,'w',encoding="utf-8") as f:
    for index,message in enumerate(record,1):
        m=message if isinstance(message,dict) else message.model_dump()
        f.write(f'====第{index}条对话=====\n')
        #f.write(json.dumps(m,ensure_ascii=False,indent=2))
        #f.write("\n\n\n")
        content=m.get("content") or ""
        f.write(f"{content}\n\n\n")






