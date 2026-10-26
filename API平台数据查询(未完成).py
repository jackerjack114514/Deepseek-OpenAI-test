from openai import OpenAI
import os
import numpy as np
import requests

client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url='https://api.deepseek.com')

#查看模型版本数
def check_models():
    for i,item in enumerate(client.models.list()):
        print(f"第{i+1}个模型：{item}\n")    #怎么只有两个？
#    return enumerate(client.models.list())

#查询API余额
def check_api_balance():
    url="https://api.deepseek.com/user/balance"
    payload={}
    headers={'Accept':'application/json','Authorization':f'Bearer {os.environ.get("DEEPSEEK_API_KEY")}'}
    response=requests.request("GET",url,headers=headers,data=payload)
    print(response.text)
#    return response

#我的文件列表
def check_files_list():
    files=client.files.list()
    for f in files.data:
        print(f.id,f.filename)
#    return files.data


#查询文件内容
def check_files(filename):
    info=client.files.retrieve(f"{filename}")
    print(info.filename,info.bytes)
#    return info

#删除文件
def delete_files(filename):
    client.files.delete(f"{filename}")
    return True;


def dairy_check():
    check_models()
    check_files_list()

