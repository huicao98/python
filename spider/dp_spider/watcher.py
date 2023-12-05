import threading
import logging
import logging.config
from .signals import Signal,spider_response_processed_singal

class SpiderWather:

    def __init__(self):
        self.mutex = threading.Lock()
        self.watched_spiders = {}
        self.sended_spiders = {}
        self.watch_events = {}

    def watch(self, signal:Signal, spider, receiver):
        key = id(signal)
        with self.mutex:
            if key not in self.watch_events:
                self.watch_events[key] = threading.Event()

            if key not in self.watched_spiders:
                self.watched_spiders[key] = []
                self.sended_spiders[key] = []
            # self.counter[key] = self.counter[key][0]+1,self.counter[key][1]
            
            self.watched_spiders[key].append(spider)
        signal.connect(receiver, spider)

    def unwatch(self, signal:Signal, spider, receiver):
        key = id(signal)
        with self.mutex:
            if key in self.watched_spiders:
                for i,s in enumerate(self.watched_spiders[key]):
                    if s==spider:
                        del self.watched_spiders[key][i]
            
            if key in self.sended_spiders:
                for i,s in enumerate(self.sended_spiders[key]):
                    if s==spider:
                        del self.sended_spiders[key][i]
            signal.disconnect(receiver, spider)

    def spider_response_processed(self, signal, sender, **kwargs):
        spider = sender
        key = id(signal)
        with self.mutex:
            if key in self.sended_spiders:
                logging.info('等待了一个spider信号')
                #self.counter[key] = self.counter[key][0],self.counter[key][1]+1
                self.sended_spiders[key].append(spider)
                self.watch_events[key].set()


    def wait_until_all_processed(self):
        key = id(spider_response_processed_singal)
        if key  in self.watched_spiders:
            while True:
                self.watch_events[key].wait()
                logging.info('等待了一个spider')
                if len(self.sended_spiders[key])>=len(self.watched_spiders[key]):
                    break
                self.watch_events[key].clear()
        logging.info('所有查询已经处理')


    def get_watched_spiders(self, signal:Signal):
        key = id(signal)
        return self.watched_spiders.get(key, [])
