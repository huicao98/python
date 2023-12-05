import os
import sys
log_path = os.path.join(os.getcwd(), 'log')
if not os.path.exists(log_path):
    os.mkdir(log_path)


cache_path = os.path.join(os.getcwd(), 'cache')
if not os.path.exists(cache_path):
    os.makedirs(cache_path)

# 应用配置
CONFIG = {
    # 尝试查询次数，主要针对是ip屏蔽
    'max_tries': 3,
    # 是否隐藏浏览器界面,True 不显示，False显示
    'headless': False,
    # 浏览器是否使用缓存
    'driver_cache': True,
    # 浏览缓存路径需要有读写权限
    'driver_cache_path': os.path.join(os.path.dirname(__file__), 'cache'),
    # 浏览器缓存大小，默认100MB，单位Byte
    'driver_cache_size': 100000000,
    # 设置指定浏览器路径，如cyclone设计器内置浏览器：C:\Users\charlot\AppData\Local\Programs\cyclone\resources\Chrome\Application\chrome.exe
    # 默认值为None，表示使用系统内置chrome. 注意：chrome版本需要和chromedriver.exe匹配
    'browser_path': None,
    'dp_dper': '7110a4d32cba8d6d217be34f1f9e67a8c41578984431ef51898290d87a4fc9d536050babee80403f75891efbbf50be49b289acceb57c0e148ccd81e7ce062bcc',
    'proxy': {
        'enabled': False,
        # 目前提供代理
        'provider': 'shenlong',
        # 可以从ip代理商的网站上生成 json 方式提取，提取
        # 选择属性
        # 城市  运营商  过期时间
        'api': 'http://api.shenlongip.com/ip?key=5d19sppa&pattern=json&count=2&need=1111&mr=1&protocol=2&sign=17ec493f956e52f8401393e66339e11f',
        # 获取代理http超时
        'timeout': 3,
        # 代理获取尝试次数，如果失败了，需要检查代理的额度、账号、api 是否正确
        'max_tries': 3
    }
}

DB_CONFIG = dict(
    host="101.132.162.110",
    port=13306,
    database="dp_spider",
    user="db_writer",
    password="1BNCe(&zAj5FAwSL*een"
)

# 日志配置
LOGGIN_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(name)s in %(module)s, line %(lineno)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_path, 'spider.log'),
            'encoding': 'utf-8',
            'when': 'd',
            'interval': 1,
            'backupCount': 60,
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
