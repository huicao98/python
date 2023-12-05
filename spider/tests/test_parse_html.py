import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib import parse
import fake_useragent

print(fake_useragent.UserAgent().random)


# r = requests.get('https://www.feishu.cn/')
# url = 'https://www.feishu.cn/'
url = 'https://www.huawei.com/'
# url = 'https://www.baidu.com/'
# url = 'https://www.feishu.cn/customers/laiyifen'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})

# print(r.text)
# logo_url = parse.urljoin(urlparse(url).scheme, urlparse(url).netloc,'favicon.ico')
logo_url = urlparse(url)._replace(path= 'favicon.ico')

print(logo_url.geturl())

soup = BeautifulSoup(r.text, 'html.parser')

title = soup.title
meta_title = soup.find('meta', attrs={'name': 'title'})
print('meta_title: ' ,meta_title)

if title:
    print(soup.title.string)

if meta_title:
    print(meta_title.get('content'))


meta_description = soup.find('meta', attrs={'name': 'description'})
if meta_description:
    print(meta_description.get('content'))

meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
if meta_keywords:
    print(meta_keywords.get('content'))

icon_link = soup.find('link', attrs={'rel': 'Shortcut Icon'})
if icon_link:
    print(icon_link.get('href'))

