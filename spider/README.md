# dianping-spider

dianping-spider

## 环境

- python 3.8.10

pip install -r .\requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn

### 安装驱动

- 安装chromedriver: https://cuiqingcai.com/5135.html

- 如果使用python虚拟环境，将下载的chromederiver放到虚拟环境bin目录即可


0. 需要安装chrome
    
    - 目前不支持其它浏览器

    - 开发环境chrome版本：版本 109.0.5414.119（正式版本） （64 位）
） ；

    - linux dev环境 chrome驱动路径：venv/chromedriver，注意驱动版本需要和chrome尽量一致，防止运行错误；下载路径：https://chromedriver.chromium.org/


### 使用

#### 先运行 scrap_shop_brief.py 提取店面基本信息

#### 再运行 scrap_shop_detail.py 提取店面详情