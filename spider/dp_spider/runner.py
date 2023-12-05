import logging
import logging.config
import traceback
from threading import Thread, Event
from queue import Queue, Empty
from .config import CONFIG, LOGGIN_CONFIG
from .exceptions import SpiderExit
from .spider import Spider, SpiderRequest, SpiderDataItem, SpiderDataPipeline


class SpiderRunner:
    def __init__(self, proxy_pool=None):
        self.is_running = False
        self.proxy_pool = proxy_pool
        self._spider_queue = Queue()
        self.item_pipeline = SpiderDataPipeline()
        # self._setup()

    def run(self):
        """运行

        Exceptions:
            RuntimeError: 已经运行
        """
        if self.is_running:
            raise RuntimeError('已经在运行中...')

        logging.info('开始运行.....')
        self.is_running = True
        # 运行spider
        self._stop_event = Event()
        t = Thread(target=self._bootstrap)
        t.isDaemon=False
        t.start()

        # self._bootstrap()

    def _bootstrap(self):
        logging.info('bootstraping start')
        try:
            while True:
                spider = self._dequeue_spider()
                try:
                    for request in spider.start_request():
                        self._do_request(spider, request)
                    spider.success = True
                except Exception as ex:
                    logging.info(ex)
                    logging.info(traceback.format_exc())
                    spider.success = False
                    if self.item_pipeline:
                        self.item_pipeline.process_item(ex, spider)
                finally:
                    # 关闭spider
                    if isinstance(spider, Spider):
                        logging.info('关闭spider')
                        spider.close()
        except SpiderExit:
            logging.info('停止')
        finally:
            self._stop_event.set()

        self.is_running = False
        logging.info('bootstraping end')

    # def _setup(self):
    #     logging.config.dictConfig(LOGGIN_CONFIG)

    def stop(self):
        """停止

        Exceptions:
            RuntimeWarning: 未运行执行，警报
        """
        if not self.is_running:
            raise RuntimeWarning('未运行')
        logging.info('停止中...')
        self._enqueue_spider(SpiderExit)
        self._stop_event.wait()

    def _do_request(self, spider, request):
        """执行请求

        Args:
            spider:
            request:
        """
        fetch = request.fetch or spider.fetch
        parse = request.callback or spider.parse

        for response in fetch(request):
            if response is not None:
                for result in parse(response, request):
                    if isinstance(result, SpiderRequest):
                        self._do_request(spider, result)
                    elif isinstance(result, SpiderDataItem):
                        if self.item_pipeline:
                            self.item_pipeline.process_item(result, spider)
        spider.success = True

    def _enqueue_spider(self, spider):
        if self.is_running:
            logging.info('spider enqueue')
            self._spider_queue.put(spider)

    def _dequeue_spider(self, timeout=None) -> Spider:
        try:
            spider = self._spider_queue.get(timeout=timeout)
            if spider is SpiderExit:
                raise SpiderExit('运行器停止')
            if self.proxy_pool:
                # 设置代理
                spider.proxy_pool = self.proxy_pool
            return spider

        except Empty:
            return None
        except SpiderExit:
            logging.error(traceback.format_stack())
            raise SpiderExit('运行器停止')
