import threading
import weakref
import logging
import logging.config

def make_id(receiver):
    # 实例方法
    if hasattr(receiver,'__self__') and hasattr(receiver, '__func__'):
        return id(receiver.__func__)
    return id(receiver)


class Signal:

    def __init__(self):
        # {id(sender), receivers[]}
        self.receivers = {}
        self.lock=threading.Lock()
        self._has_dead_receiver = True
    
    def connect(self, receiver, sender=None):
        key = (id(sender), make_id(receiver))

        if hasattr(receiver, '__self__') and hasattr(receiver,'__func__'):
            receiver_object = receiver.__self__
            receiver =  weakref.WeakMethod(receiver)
        else:
            receiver_object = receiver
            receiver = weakref.ref(receiver)

        weakref.finalize(receiver_object, self._remove_receiver)
        
        with self.lock:
            self._clear_dead_receivers()
            if not any(key==r_key for r_key,_ in self.receivers):
                self.receivers.append((key, receiver))
            

    def send(self, sender=None, **kwargs):
        logging.info('发送信号')
        receivers = self._live_receivers(sender)
        for r in receivers:
            logging.info(r)
            
        return [receiver(signal=self, sender=sender,**kwargs) for receiver in receivers]    


    def disconnect(self,receiver=None, sender=None):
        key = (id(sender), make_id(receiver))
        disconnected = False
        with self.lock:
            self._clear_dead_receivers()
            for i, (r_key,receiver) in enumerate(self.receivers):
                if r_key == key:
                    disconnected = True
                    del self.receivers[i]
                    break
        return disconnected


    def _live_receivers(self, sender):
        self._clear_dead_receivers()
        _sender_id = id(sender)
        receivers = []
        for (sender_id, _),receiver in self.receivers:
            if sender_id == _sender_id:
                receivers.append(receiver)
        
        none_weak_receivers = []
        for receiver in receivers:
            if isinstance(receiver, weakref.ReferenceType):
                receiver = receiver()
                if  receiver is not None:
                    none_weak_receivers.append(receiver)
            else:
                none_weak_receivers.append(receiver)
        return none_weak_receivers
            



    def _clear_dead_receivers(self):
        if self._has_dead_receiver:
            self._has_dead_receiver  = False
            _receivers = []
            for key,receiver in self.receivers:
                # logging.info('remove rereceiver....')
                # logging.info(receiver)
                # logging.info(type(receiver))
                # logging.info(isinstance(receiver, weakref.ReferenceType))
                # logging.info(receiver())
                # logging.info('<<<')
                if not (isinstance(receiver,weakref.ReferenceType) and receiver() is None):
                    # logging.info('remove success')
                    _receivers.append((key,receiver))
            self.receivers = _receivers
    
    def _remove_receiver(self, receiver = None):
        # logging.info('释放receiver')
        self._has_dead_receiver = True
    




# signals
spider_response_processed_singal = Signal()