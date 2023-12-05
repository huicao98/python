class SpiderExit(Exception):
    pass

class SpiderBlockedException(Exception):
    def __init__(self,message=None):
        super().__init__(message or 'IP被锁定，查询失败')

class SpiderQueryFailException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '查询失败，请重试')
