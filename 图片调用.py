import base64
import os
import pandas as pd
from openai import OpenAI
from urllib.request import urlopen   #url图片链接
import sys
import ssl
from urllib.request import urlopen
from urllib.error import HTTPError,URLError


client=OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")

#https://www.i.u-tokyo.ac.jp/upload/focus_sadakane-2.png    #本地图片
#with open("C:\\Users\\Administrator\\Desktop\\Deepseek接口调用\\CA证书密钥泄露排查.jpg",'rb') as f:
#    b64=base64.b64encode(f.read()).decode("utf-8")

url="https://www.i.u-tokyo.ac.jp/upload/focus_sadakane-2.png"

try:
    with urlopen(url,timeout=10) as pic:
        b64 = base64.b64encode(pic.read()).decode("utf-8")

except HTTPError as e:
    print(f"[HTTP错误] 状态码:{e.code},原因:{e.reason},URL:{url}",file=sys.stderr)
    sys.exit(1)
except URLError as e:
    print(f"[URL错误] 原因: {e.reason}, URL: {url}", file=sys.stderr)
    sys.exit(1)
except ssl.SSLError as e:
    print(f"[SSL错误] {e}", file=sys.stderr)
    sys.exit(1)
except TimeoutError:
    print(f"[超时] 访问 {url} 超时", file=sys.stderr)
    sys.exit(1)

messages0=[{'role':'user',
           'content':[{'type':'text','text':"简单描述这张图片"},
                      {'type':'image_url','image_url':{'url':f'data:image/jpeg;base64,{b64}'},},],},]

response=client.chat.completions.create(
    model='deepseek-flash',
    messages=messages0
)

#print(response.choices[0].message.content)

output_dir='C:\\Users\\Administrator\\Desktop\\输入输出流\\图像识别'
os.makedirs(output_dir,exist_ok=True)
filepath=os.path.join(output_dir,f'图像识别结果-{url[8:15]}.txt')
with open(filepath,'w',encoding='utf-8') as f:
    f.write(f"{url}\n\n#==================================\n")
    f.write(f"{b64}\n\n#==================================\n")
    f.write(f"{response.choices[0].message.content}\n\n\n")