from collections import deque
import threading
from datetime import datetime
from time import time
import logging
import logging.config
import requests
from datetime import datetime


class ProxyEmptyException(Exception):
    pass


class ProxyProviderFrequencyException(Exception):
    pass

class ProxyProviderInvaidException(Exception):
    pass


class ProxyObject:
    def __init__(self, ip, port, expire_time=None, *args, **kwargs):
        self.ip = ip
        self.port = port
        self.expire_time = expire_time
        self._is_valid = True

    @property
    def is_valid(self):
        if self._is_valid:
            self._is_valid = self.expire_time > time() if self.expire_time else False
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        self._is_valid = is_valid

    def to_str(self):
        return f'{self.ip}:{self.port}'

    def to_repr(self):
        return f"""
        ip: {self.ip}
        port: {self.port}
        expire_time: {datetime.fromtimestamp(self.expire_time)}
        """


class ProxyQueue:
    def __init__(self, *args, **kwargs):
        self.queue = deque()
        self.mutex = threading.RLock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)

    def qsize(self):
        self.mutex.acquire()
        s = self._qsize()
        self.mutex.release()
        return s

    def put(self, item):
        self.not_full.acquire()
        try:
            self._put(item)
            self.not_empty.notify()
        finally:
            self.not_full.release()

    def get(self, block=True, timeout=None):
        self.not_empty.acquire()
        try:
            if not block:
                if self._is_empty():
                    raise ProxyEmptyException('queue is empty, no block')

            elif timeout is None:
                while self._is_empty():
                    self.not_empty.wait()
            else:
                if timeout < 0:
                    raise ValueError('timeout must be positive')
                endtime = time()+timeout
                while self._is_empty():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise ProxyEmptyException(
                            f'queue is empty, timeout is {timeout}')
                    self.not_empty.wait(remaining)
            item = self._get()
            self.not_full.notify()
            return item
        finally:
            self.not_empty.release()

    def _is_empty(self):
        return len(self.queue) == 0

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        # fifo
        return self.queue.popleft()


class ProxyProvider:

    def __init__(self, config:dict, *args, **kwargs):
        if 'provider' not in config or 'api' not in config:
            raise ValueError('IP代理商没有配置')
        self.config = config
        self.max_tries =  config.get('max_tries',3)
        self.tries = 0 
        self.mutext = threading.RLock()
        self.not_created=threading.Condition(self.mutext)

    def create(self):
        self.tries = 0
        while self.tries<self.max_tries:
            self.not_created.acquire()
            try:
                return self._create()
            except ProxyProviderFrequencyException as ex:
                logging.info(ex)
                endtime = time()+5 # 5s后再请求
                remaining = endtime - time()
                while remaining > 0:
                    remaining = endtime - time()
                    if remaining<=0.0:
                        break
                    self.not_created.wait(remaining)
                return self._create()
            except Exception as ex:
                logging.info(ex)
            finally:

                self.tries+=1
                self.not_created.release()
        
        raise ProxyProviderInvaidException(f"代理{self.config['provider']}错误")
            
    def _create(self):
        provider = self.config.get('provider', None)
        url = self.config.get('api')
        response = requests.get(url, timeout=2)
        return self._parse(provider, response)

    def _parse(self, provider, response):
        logging.info('解析代理返回值：')
        logging.info(response.__dict__)
        if provider == 'shenlong':
            # {"code":"200","data":[{"ip":"114.223.3.141","port":"33283","prov":"江苏","city":"无锡","isp":"电信","expire":"2023-03-09 14:29:07"}]}
            data = response.json()

            logging.info(response.json())
            if data['code'] == 200:
                proxies = []
                for pro in data['data']:
                    proxy = ProxyObject(
                        ip=pro['ip'], port=pro['port'], expire_time=datetime.strptime(pro['expire'],'%Y-%m-%d %H:%M:%S').timestamp())
                    proxies.append(proxy)
                return proxies
            else:
                raise ProxyProviderInvaidException(
                    f"神龙代理IP错误，错误码:{data['code']}")

                    

class ProxyPool:
    def __init__(self,config={}, *args, **kwargs):
        self.config = config

        self.timeout = self.config.get('timeout',3)
        self.queue = ProxyQueue()
        self.proxy_mutex = threading.RLock()
        self.proxy_provider = ProxyProvider(self.config)

    def get_proxy(self) -> ProxyObject:
        self.proxy_mutex.acquire()
        try:
            try:
                return self._get_proxy()
            except ProxyEmptyException:
                pass
            # 创建proxy
            proxy_objects = self.proxy_provider.create()
            for proxy_object in proxy_objects:
                self.put_proxy(proxy_object)

            return self._get_proxy()
        finally:
            self.proxy_mutex.release()

    def _get_proxy(self) -> ProxyObject:
        proxy_object = self.queue.get(block=True, timeout=self.timeout)
        if proxy_object:
            logging.info(
                f'>> pool------> get------------>{proxy_object.to_repr()}')
        return proxy_object

    def put_proxy(self, proxy_object: ProxyObject):
        if proxy_object and proxy_object.is_valid:
            self.queue.put(proxy_object)
