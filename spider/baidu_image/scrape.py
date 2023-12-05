# 获取点评评论
import os
import time
import datetime
import requests
from fake_useragent import UserAgent
import uuid


keyword = "船舶"
offset = 0
page_size = 30
path = os.getcwd()

print('--------->',path)
path = os.path.join(path,"log","baidu-images")
os.makedirs(path, exist_ok=True,mode=0o777)
while True:
    res = requests.get(f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10325698282751932769&ipn=rj&ct=201326592&is=&fp=result&fr=&word={keyword}&queryWord={keyword}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={offset}&rn={page_size}&gsm=3c&1692000116636=",
                    headers={'user-agent':  UserAgent().random})

    offset = offset + page_size
    images = res.json()
    if images['data']:
        for image in images['data']:
            if  'middleURL' in image:
                print(f"image url: {image['middleURL']}")
                r = requests.get(image['middleURL'])
                file_path = os.path.join(path, f"{ datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')}-{uuid.uuid4()}.jpg")
                with open(file_path, "wb") as f:
                    f.write(r.content)
    else:
        break
    
    time.sleep(1)
