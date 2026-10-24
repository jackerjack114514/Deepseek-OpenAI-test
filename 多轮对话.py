import os
from openai import OpenAI
import time

tm=time.time()

client=OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")

message=[]
flag=0
while(flag==False):
    question=input()
    message.append({"role":"user","content":f"{question}"})

    if question=="结束对话":
        output_dir='C:\\Users\\Administrator\\Desktop\\对话记录'
        os.makedirs(output_dir,exist_ok=True)
        filepath=os.path.join(output_dir,f"message-{tm}.txt")
        with open(filepath,'w',encoding='utf-8') as f:
            for index,message in enumerate(message,1):
                m=message if isinstance(message,dict) else message.model_dump()
                f.write(f'====第{index}条对话=====\n')
                content=m.get('content') or ''
                f.write(f"{content}\n\n\n")
        flag=1
        break

    response=client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        reasoning_effort='max',
        extra_body={'thinking':{'type':'enabled'}}
    )
    print(response.choices[0].message.content)
    msg_dict=response.choices[0].message.model_dump()
    message.append(msg_dict)

