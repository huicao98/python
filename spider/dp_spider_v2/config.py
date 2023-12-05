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
    # 是否显示浏览器图片
    'imageless': False,
    # 浏览器是否使用缓存
    'driver_cache': False,
    # 浏览缓存路径需要有读写权限
    'driver_cache_path': os.path.join(os.path.dirname(__file__), 'cache'),
    # 浏览器缓存大小，默认100MB，单位Byte
    'driver_cache_size': 100000000,
}

DB_CONFIG = dict(
    host="127.0.0.1",
    port=3307,
    database="db_spider",
    user="db_write",
    password="^&hkj2ja7$1JH@G12*&z"
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
