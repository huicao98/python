# 获取点评评论
import os
import time
import random
import logging

import dateutil
import plyer
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from config import CONFIG,LOGGIN_CONFIG
from browser import BrowserFactory
from mapper import ShopMapper
from get_dp_cookie import get_cookie
from plyer import notification
logging.config.dictConfig(LOGGIN_CONFIG)
import requests
from fake_useragent import UserAgent
from urllib import parse
import dateutil.parser

from dotenv import find_dotenv, load_dotenv,get_key, set_key
load_dotenv(find_dotenv('local_env'))

class SpiderBlockedException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '被封锁了，请处理')

class SpiderVerifyException(Exception):
    def __init__(self,message=None):
        super().__init__(message or '身份核实，请处理')

def get_dp_comment(driver=None):
    
    行政区=['南山区','福田区','宝安区','龙岗区','龙华区','罗湖区','光明区','坪山区','盐田区','大鹏新区']
    地区=[]


    base_url = 'https://m.dianping.com/ugc/review/reviewlist?yodaReady=wx&csecplatform=3&csecversion=1.4.0&optimus_uuid=18991a880ffc8-19a33c260111d9-0-0-18991a880ffc8&optimus_platform=13&optimus_partner=203&optimus_risk_level=71&optimus_code=10&tagType=1&tag=%E5%85%A8%E9%83%A8&offset=0&shopUuid=iuBoFzreao26iC1K&cx=WX__ver1.2.0_CCCC_dfwOgF35EQNYzVh8i27kXL04k6XTiM6UIbLC34PDQwAlFFunePPYPkpJq4XJVRltidhrJWr7r1NZY58S2zwZNLhDW3M0QlkFrcE2pVHRnPzhLCmMZ07fFkSGcYn7seWOp2qiDmCMz9sGQ8X2SU%2B6Dj8eSpU5CGKGLIUvYfzpcbwMU9g6W3gif%2FPyGyBT3Ah6VQ%2FjCoafjv9hiWbjdc9ZE7pY6iK%2B5e4Dj5708qKTBwhoaaFZn%2Bm2Dl4yQdKqDuImIwQvb0EUxmHFQbGj99%2BrKo59BjATtfJye1Of0Hk1AoWnIaBgDWONjLiWsiwz1YKK8wdIw9FcV5fx5zniOLikqGhXS%2F4NY83UKdeetrEXb0a6uL0qRheEJNXQZoCUoiCmdvk6zlvmbgPQySDDmhWK84XAzszOht%2FFIWhAfJxFb2XmsOozr9geq7Dhw49cyWLxkIPU8q6BXyXh71JiGs8Q2mLfT%2FGTZlns2oQlOArCdaasR%2BXlkBZ7rJAf0Mo3KKOqSs%2F1hABJIWdd%2FQp%2B57n2bNjXrB1Th23nw8dST9D83z%2F4rFQrsAQ0MB89xxf2cPimgRqZbIYnj6a1d5QBKJZpTosGgJiGm6%2B0imaxd%2FtZ12bwY8LLrt%2Fcvsjux3ezf6mKdm46uiR9zfoqjnbJFx6VkbU%2FDT%2BPKHO689ufFYI1ANktUm9b%2FvCmetYhC9M4fURUvxWn9JNt%2BVnCmRrH48TeYsvjGBsrot%2FA6rjktYQs%2Bq6qL%2BcTT3TsmYcDT4F7JQr%2FkTffF1%2B2mOOlK5WELtgjpxuSMCzCSlHUzybZNYJ6oD%2Bs2alpWVXDdciW7UxlOXyJOeEJDpJ6CF%2FC10Bz6T8EH3EOyIItIyHWnXo0XwGEgJRSY7tQiNM1yk5EUey2FCXE5BD5NLiq6VO174kwEVWpU1ctF6Vt0w0oytTbE57ywcyyx%2Bt3Vz1XA7hKP%2BFYDtf5quFSCgRv70kvEG3qZnsJ0SH8LjYvqYzWiOwpOK1lNZW0GDAlVSz5%2Fuvpb5JG4iSoU3NBj1RRWLJ%2Bosz2m0BrYSYc%2FMVLDR3yqy%2BsWEHYSPBXnF5TS%2BHcLzeWvWLsx3S4IvC6hLXcTL%2FJHcMhyzYf%2BFkMJujFqf%2FOsZp%2FrKyAhKmZ0TzlPxNWDn18X4vCzWK%2BIZbEceniBeSUk0%2BbUH5cW7kxptGZSCe5%2Bk1Wjp1k8poLdHXPSBfmuISH63YI2T6CYxTJmcJBEuJrns1TW95gMA4gdGkLET8ZCwMUgFCLWcz8x1x9ipsD6AFA1vLDWTRPaJC5WzXxktxtOaika8E35w0b5AIfQOQz%2Fz0gbipqT%2FNgZBCCsOf8ekLgjnY4DjZvqrp2svy%2FNCjthBUcDdCXXGSkT0Hj%2FfGdD0eDon1Q7HfP9C61DyG345DKzmRikmwr9Xv5q1YKuBtQnHu8nEwSgigPjgDCdDbJeApQ36Efqx1bOUXfV%2FakcUvy5NvR%2FQm%2B%2B4i3V07KmEI%2BpL1TIiat%2Bo%2FYyZ71PcVsGm2I4h%2F45h1tiZnyVxYZvrPw7PRKk7087%2FBDcq5FiCPRLkU79X7RvVk7jvwckTibNIndNuYy%2BvBcQ1WeJJpbEtje%2FhJLNkzIPx1H%2BNClgHYbRAX4%2Bfgs%2FBeAPrlm%2Bv%2Fr2CWj0ALn%2FKEWYwlXYwjj5NIG5efwJ21m4f36BZkCb0ZmA933TQ%2FNVlHE8fB5XRY7QxgumdLwD2oUA0KlSzSR%2BFfAwT3iYB9YEid6BQ1S5owANfDAubWQ%2Fz8VxfFZTWz0la6J0kgY0u6YPswTI3Yu8btsDF%2FYuFiOvqvxlQFDccp5ELwnwGEU76tzhvaPteTclGcAsnS2byekeJNLat8SGlBqdMQjBf5ixuXt5CdezDQGOUoZymlY8HyYZmUv%2F%2FWpqFC4q1dJ5dWkZzJfrrHLU0J%2Fqo%2FiLHcCKyL15%2BlKx6kTYosqvSdeIgEPr8S0CEkRUO4E0qN3T0T45ayMOPDP9LSdkaa5xfYg&mtsiReferrer=%252Fpackages%252Fugc%252Fpages%252Freviewlist%252Freviewlist%253FshopUuid%253DiuBoFzreao26iC1K%2526msource%253Dwxappmain%2526tagType%253D1%2526tag%253D%2525E5%252585%2525A8%2525E9%252583%2525A8&_token=eJxNVNeupEoS%252FJd%252B5Uh4N294aJoGGs%252FVfcB771ntv2%252FP7kh7pSpFVlYopayKjH89ZiV9%252FIJ%252BHuvy%252BAUTNErRFEnDJEz9PJJ%252F5CgIhSHk5xHPLv%252F49RcGEz8kSv39O%252FH5nv%252FCEeiHRtC%252Ff%252F4fIdh3%252FWYoX8JjjJImKrIF3IoEHP8bzdleZUdbLes%252FwsfP43%252B341D93o9vhc7%252BVvhi8wejP7j%252BwaUq%252BsevR%252FY80%252FaV66RWfMqUbot86dlnnLE%252BzRj3h9cuS37OXUHT2O1nX8biOAQHQSmcqCODqXQIcUBtm5PxjpMeJ8EFyLM75vdLB80bwG%252BwC%252FEh%252FVRcsXnyeOzQNplLLcEXtyj%252B1WelusnSklRjR6U2t6oSTofjxCLBrZZGrwK0t7nurFd1ZmvEJTMOGV4yImxtfMn7JMyv4INDH%252Bbc8xoOV3Ty5VTDbMWXzkU1WyJZGiqArK7aAAyHoL1pfLzSIY4VabuzEULnsrGpIjLD%252BTw4ldzGk41jqHUqD%252BgFtJUcmmMVJyK8Hiaeu3qLOz6MtFx5KDjbWC3TVxJlu7q5Wo2%252BnR%252B%252BFZqyRs1vby%252FfjSZ7P7oUfJakLTSblKOCCgdT10Td22FHuouSNEw2%252BxVcqigzt87D1PLxQC4b0jTCLdRNEp2d2qeslgDUve4T1Ox9r1VoGrsGmlPWZqgBFn37Ja79EQBl9S6gSJ7cLuKHvXT0nl8d%252F5lvvC%252Bh2Zn4Y%252B%252BHxhtw%252B2b8Pq%252B2r7C0DVxJPkNtHs%252BizuckOG7U%252FtjRJ5fbIpWfOLL2ytisb1Zf87zpOaty1lZxIW8jmKbUETBQNLdbDg1PJShXOPAVlib69Dr2JPipmqRRpwuZfy7KvIxWO9Qmq9NNtcAgqR0N8RwMmB3jkKfOD1HQxeLtBue9OXvM6vt%252Byt8%252Fnqt34J2yYcJCIozxLE3CQOqLUIv41aSMw7oiDo2bEhxCSbGj199cFZNOR%252FXdCuFQ1I7lKcZ09NrzZz0ZbSw0aIEu5n7xHTfxmF58Ne0zZ9vRUgjr9yClBPmCJ74huMzbLho1SCRzd9PNjDSh8SGXdLc54pcvzLt2HMN1igcaIcx6CB9N%252Bg4Gvw2LH%252FIHX0VWVXt8HRq9UhxF70mQumFPpJ0djOxDGyA70ohLtE0SYhA5nr8ORRTIrAO%252BWjRUhUbud36%252BNJvMr4BSj6ApWMhYbLtyKIERMfzVujGW%252BRtlNDKtmJNEkQqbzM4IHm3GcwiOKNar5%252B76hZGjZyd2XAjdogcW%252BibHYxlmIcMcPXqV3vMMD6qeLOKeWNFH80UDzNEbuGDhdt3G12GB3BlHhK5FTIjrF%252FHwLhn%252FeCy4OKiIt7Kql8cEZdnICxqAxnsvHgiVBO5lLUuR%252BHDaRPkMUbYpSbgTENUT4nWoZnB4r32ggP2Er7gAZN5tB4qoLLMl8Uy7PCO7%252FlWlU7DLb2HKu%252BeAyaqCdh58ok3xLqg2grzxPKC2Z4QQdCtrdl5Klm63a6AAS3S5dPdxQ4k4z3jNdO2IdiLSUSmomWWZ9LnraXGQ9pKYA11gy0gcXS9GE8zXd0chiE2aEcfWfCF8xaZDlaOqyK2iHHBgtIhRnnUooxPZPjc0xi58KvHqxjyBmS5PeWczNEnhX%252Be86xl1C3WZ6CByIwHtXvrUDYXlGBcTjNcnobYj3jmpmovoeeROhfPtpvnKFN2fah4MYxMsctUoZVmBwh79%252BfLnZ3%252BrQIw374OEJk1MrL4ZMCzJ1qWU41VJmFz3S0nBZppMJ2QiAiKm5ZACzFg9J9oB39Pg8%252FN3%252FGdtyziyDS63%252FhRLW8oHgaXlAebH%252B9OgFVlmG3mBJlEwzEQz6EedUoXRa7ZeLzFCGYYJfUt7dlRLNPwoncJiH0JLzMsLzMKT3xa0M%252FFmXY1VVIrqyu1XGSRZ%252BIrgy6KX3gc7UslqwDqntvIz3M7NZQukxObA4Pp82jqIoHsRTWiP25bCzLzQCPi0dMXHLoPxu7OQbqmTjZixF0zBT9%252FEbq8g5oJ18pmF0hQjhwVzW0Bl6iSwW3WRZP50%252BUCzra9io2GnN9nUnYWcKQ6qp9fsbHABJVKLyQ48k6v4dYlblwo34a3C5VpW2tl3jSX1k7xvNiTFvrTJW%252FNNKiMHO6hEtRiZrqiZXsNltnm%252FqzETYUwoIGSpZTS66cACLDNMHIEEFmDaKutENyfrvL17qoijCeuugJL7DrsqokUVcV8ve%252BvtaW2SmSLfPipst0dmTXGinApsfFTLYmCl29fH3hBWlRB8TBs3wpiFNgt4m6hWsuEhLW8l46I0k4aDn%252F3Bqj%252BadpF2HFmBX9St%252FV7M550ssMZIUfq2WJm5jHlKS6qKVsRr7E9ehSzl%252ButFuiq13Vny9a4TUHQhfAqnH1Jdhyp7%252BwKeexerwDUQiEf7FCuG6SW9kdXqgSJ%252FeWeB1oZnm8VH81miAATiGZYdbizafesRe5GTPoBEObj31xWcTQKJ1KBNmWHB055cRBp8qAbN3dxBdr5yrfdioJ53lMxBAETouO8BHAQB453n4I3TH4CPwQrND82Zt6h5%252FPs%252FRhw%252FXw%253D%253D&isNeedNewReview=1&device_system=WINDOWS&wxmp_version=9.40.0'
    url = parse.urlparse(base_url)
    query = parse.parse_qs(url.query)
    del query['tagType']
    del query['tag']
    del query['isNeedNewReview']
    query['offset'] =['{offset}']
    query['shopUuid'] = ['{shopUuid}']
    l = []
    for k,v in query.items():
        l.append(k + '=' + v[0])
    qs='&'.join(l)
    new_url = parse.urlunparse((url[0],url[1],url[2],url[3], qs ,url[5]))

  
    while True:
        shops = ShopMapper.find_all_unscrape_comment_time_shops(行政区=行政区,地区 = 地区 )
        if len(shops)==0:
            logging.info('******任务执行完成啦************')
            break
        try:
            for i,shop in enumerate(shops):
                print(f"total: {len(shops)} no: {i+1} shop: {shop}")
                _run_get_dp_comment(shop=shop, driver=driver, url=new_url)
        except SpiderBlockedException as e:
            notification.notify(title="扫码登录", message="点评重新扫码登录", timeout=5)
        finally:
            pass

def _run_get_dp_comment(shop, driver, url):
    # url = "https://m.dianping.com/ugc/review/reviewlist?optimus_uuid=189b5a8742cc8-1f0e92a62bdd46-0-0-189b5a8742c52&optimus_platform=13&optimus_partner=203&optimus_risk_level=71&optimus_code=10&offset={offset}&shopUuid={shopUuid}&cx=WX__ver1.2.0_CCCC_QZ%2Bjty4uCzVN9G6PMudx0yf1ymr1r7UEqaKRtVdDWv6Y60VJG9iNo56N6%2FBslnnDMzPkRLmWDLwxiTFbh79nLRVET%2Fk0qQS6mMqBua8ngb1bfQn54Zv0zYsRQgcngXrCebeaT%2BSTMVZ%2Fylfz6V4uMYD1j0FPRR4QLWAGGiyh109ET1jfaZT7c6B6H37SFAcfYVoYlf0Cepo9cuZ7NZ057PgltxyU7FYGKgoFtSD%2Bx8YORVbfymOSIBgdVZprZDs%2BC%2B5XSV3mvB%2BZdj90hxgU9r%2FY6X%2F2di8vRlMQ7qjri6CK5nQVFy5jeNkaB6oPq9gpR8Il8RwQcTUzY46mjlul5mGZabT6BXp14ExVwwjJb0cal0DgRQ5IAUYYuUe4Pg6uLGC3b1N78MPAPGDLp7XPKzVbOqEWCqqks%2FyiKhQwq27y5PN4eLVtJSYepyaJvwLy%2B0UnRGxdEmkiZ4kBAHQ4BXGP0ESWTYQW9SyTSv3T830989qLuwM1redyrOiDoW9MvRb3pmVq26mO2rUYv5fDyqnBoyOYmJNMsclMHAzQO1C0KzR0sW0OOSQ29x9roCVVyxwIgELwXvfsvEn%2BV35sGUu%2FGq%2FT5%2BaeisA869mvFFCSq7rblcbJ%2FA8CDJ5%2FlJkn%2BTvoBi%2FqxYmo1TlGTJ43bHd8Atii%2BYBWs%2BoWfpcIdoiAHtNlYTicyGJ18EWc7qTL5qqUZ%2BCyonyORD%2BpZ43CghIGuFVxpI6pzC9nCmZ1TPWPJlrOkwnwVrxBMvoJW%2B7ueRi5qe6rclfzOhuXjWnRs1qCWs4gvvXIgHRE3AzbS%2FLVX4%2FWUtahl9tyuCnECpticbw6nachzhJcPJrs4kgGhUxh1jRBMvbwiuiv61DEZGl7F9CM9XhK79W0gC%2B%2ByW4VPr7%2Fl8x%2BqM6%2F6ChWqs%2Fw%2FiwC0dWFKyNRYI4TXQ%2Bvvmau2gbpWEsqBZqA8bPbZnJALOn1AhMv8HaAPiUeYOczMWocGfFFDuLQM10wzOa23wOOh4mlyhVN8nrOipXtI%2FZTV97TnEA3Y2cMZvHTjDIXhHl2RuAFnovSalK7jnkyXBLJAWzPaEkjmMmex6p3BtsHlHNSCWu5IS%2BFGCTfajr0zfOd5lTrs2puPlqhT7ssWS4c5jAvRu5%2BBXXoBqWLO%2B0jRoLPMNzefVriGOo8bQxUCGNwCDlpj8xKuKxtNMk1j8i2JMlWSsftzVeXE9Ep3f9C9Yox16LWsRX4I7ywJPHQyDMN5tsLFi%2BSDMJYkZl24R7ertRbHxS28pFEce2IUwwrp0UqRBt2UU%2FGAOJ%2FdIle7qYSQq40CbV88Cqs4d7zs3y7CfH59q2HTFovIUOlzAzRxIU9f4AXVBE5aZ5ULWUXKyvLV14NYmcefCCY%2Bx4ZlkL81aBTlfMrQ%2B9yWn2cIso5GM6TbBpsdkNOtN7EkUuABnYdIYWcvUd9oV%2Fb0Wtfq2VmLnJkdVUKJwhfGCGgATZwG4I0dhYm6NOq69MLXAN2mvlvCGGb9cLx%2FDoCPlYzvHTezvMlaae1YMQmkYyGA1r0X5LfQCvxzpMazm%2FwdiQ2Tj2Gevc%2FsHd41%2FkaIVzUUiporT7XH0zRETZ1MsqPwtsuH%2F1a9X5gMIFFtoOGJee1AKC453ed7vS5JzR80JXwS4QPnzGh5xETogW4INuDUrtlEaAG6BbJVI0Vkbb3dHwenxe7DodhuUJMnrSuppUFeqxrS%2BbuXjdJpTHptPWTp0p45gwb2g2R40YTlZJDO99fxjiU%2BixnEh8MgwwMSGtlHm0ALSsiRfelfC9QY8Do3ac%2Bes5F1iwwQ0ZHDzRf3xk25A%3D%3D&mtsiReferrer=%252Fpackages%252Fugc%252Fpages%252Freviewlist%252Freviewlist%253Fmsource%253Dwxappmain%2526shopUuid%253DG7kQ8cIgaZMY58Ma%2526tag%253D%2525E5%252585%2525A8%2525E9%252583%2525A8%2526tagType%253D1&_token=eJxNVdeq7EgS%252FJfzqgtqeem%252BybW8V8st%252ByDvvdew%252F749uwMzUElERiUJRaX542eRsp%252Ffr18%252F2%252FrzG8KpF4VTJI7ACPzrJ%252F2HRmEI%252FqJ%252B%252FSSLx%252F38%252FhcKob8IBP%252F3n4L99f8W%252FmYw%252Bj1%252FRkjfgJ8pTtu4zFdwL1Nw%252Bh9b8qPOz65et3%252FQn18%252F%252F7%252BdxvpP%252B%252Flm6N1vhi%252B2f2H8F25%252F4VqXw8%252Fvn1y%252BsvbJb0IrbbtIb74gsZqppapxcjqDaAs%252BaMDidV21fKJ0Ea3am9ODTxBhxlbwWkjr10MvpEUHHZJazeIgUvIaALFoM2DtgKclH3ojlsonVsLvPzVzzN2EWF7KBDqpPWghu6Aq%252BypgkqJFXbesv%252BctFDg9O9v3EB978YHhcp0KDcPcarFf5Vzuo3cDWrZKfP8iQyLzFbg3HpXhUWUlCyuWij1VRU3bETUUkkeWyOwUo496Kse2VBdHIZ9WMotWYMJ3P85mDSuUFzC89iFIdZckNJNSKwLNskpGXaspKT5Vh4bFM50RR2brm9U0bYJNBwh4Xr08i2DjwaSdMMYxJ3hDeQ9fshO9Uei52BfNwixDuDA%252BWEJN8BADeT0O0beQ03Ttf5Ddm%252Ff4Mp08xi4qTJCJtQv4WT59dHBMr1T3xteTHCOcyyAI1wlkTmRJjXj1m02Np7SaxlSG7LoOIxSdXfLRVyNddZBwqag%252FENtcri1G9ikvjNLGG%252Fu%252B77bkr%252F2A%252BQGpiyCO%252B9In8S7rxEpnA7muxmSol0TKsF3zbnCvApprqSlCo%252BEJIEaMNdN1bbmjdZbLqe9fUuxApPtDoRFt1qwyOVlrvCPiIeQF6quNdDZ4w7g3jIxuOYSElixVwwSZbrp6mm%252BN3C9zuxRzm0CG6OcV5FNcbRHT3p8V9DlMOt8wSOxUWXnl55s8DArlkJNJbOTDXHT10mpTx8dPn%252BJDxIQGLPeyBru%252BY8ldZ1wr4yfDQsNW3jNz%252BhB0EsYfT7QrUNZuc9pinGlNPghNVtUi%252Fx7juJipWHAnKB%252FL2z1k0mlxvXwBtkCLqw7GXiJyjIBL2qa8hpQxyFQObtKPp2E%252FK5jTAQuGuqM5iBObdJt6iTDtq%252Bpiz0k6XIZJ7IMHHSc1bEvpFH5AMTdyGlPxXsiSQF0Bckia9qgMhZeum48mh7CsexadG06zxZcdk10LQ4ONHd5381oAAaJMWWmQfcyqpwX4bmPHd%252B2x8xhYRWfdlkpjsZFrtl46GEFPhlQ%252BXQJsEi36DLl25sDilLJ%252BeCU7aRc%252BwhWZ%252BEsYILKXp2nUGsGZ5Wyyc6raOxkhq8G1d6QfIyKfG6ANa15ClDhUyjPbLrRpXmagEPaykIt7m%252BgDuu9QdpnblKYznzCg4uvZPg43D3Tnw0HJpU%252FjaFOwAWPFpW7HMjJ2pM9gE1UHMiEx5qSAOVVQnkTm4ycUF%252BmrxTDRhDaFhlhBPsbQs5wlCsevD%252FCxbkBNYmmm8AyJNYmWy1GICv4jjmoKKVI8I8FQPYk%252FcrBdDzW6xGWhbrmRmG8wwaET2kKxiCREivcjcQgxDyrifHMkwI5zd%252B4Cn6ZesdCsVxu71cQZlsazsIRrDUmcPgdqaH%252Bb3W8tYIGS2xRgXqQ%252FwGOLshliWKU%252FctglfPYRbKj%252FnC01pz2vJsOblVz3diIlfT9hReTeyfvPecWtkjcNt7bzjugIlEyA7TCfUfyWYZOGDlbvpLDAW2AyjXfWhM5ioV7ahg63YYVG1QW3SuaGLA4ymDz5AW0zHsL3Ubq2ieuhSCkgedO7hDbpjJk9ecOUlCaJ5Cav7tK9v92%252FUtT9ybxaucJXi71qpeQjLwjRaATQyJkZ1REycSdWXAk%252FSneX20MLPYQWrzhBiCO%252BBt6o8CXSc757HbTGRJXTGxeAzFqMXBAaqb5sCBT%252FmOknkNGIHb9rRuwRnEoajdt4UrL3Gklr%252F%252F3qUagOCGtgNdsrJ2eUz2YZx%252BkZNBOqP%252FltR6S9h6C8tRGdilw0C8dr876zxXiZ04gpcJrj5DZcWv3U7i2jfP6BHVNVh7bIBndgOK%252BH98WMnyOEGwVwXSPbaPLoy9498QfhoULIebuylua0Jt7a39ac6xGPD7Mhk9CNWcMDFa0%252FYaIybssOPyXcvIN%252BXm59Z6f0tjApEgdaxcqyOwv77N8cjMH3mEeoXlJmgXgE9HWwCfDFLsdeBQIywYYQMXkrBYY8ADjyUoidcBq1xwBs%252FjSQHdiaT3BB2xE%252FIHsClY9Gm3toBQegKIqIK7osYJkzqh4%252Bu9fnxcaXL3nqlMi%252BJ%252BkTz2Sc49fuDyRtMrlxuvcbYOSBrChrLQrAOCIShcBJEQ40rn1ThQTUB64Z2vZcHA90R4NCOQwvFwxzTcD%252BIMAC6IML2AgEBFCSAsFCHCAKuL9vOcAzzu7ULH7%252B81%252BGDQ8B&pullDown=true&reLoad=false&device_system=WINDOWS&wxmp_version=9.37.4"
    first_url = url.format(offset=0,shopUuid=shop.code)
    data=_request(first_url)
    review_count = data.get('reviewInfo',{}).get('reviewListInfo',{}).get('totalCount',0)
    print(f">>> review count: {review_count}")
    last_review = None
    review_list = []
    if review_count:
        if review_count<10:
            review_list =  data.get('reviewInfo',{}).get('reviewListInfo',{}).get('reviewList',[])
        else:
            last_url = url.format(offset=review_count-1,shopUuid=shop.code)
            data = _request(last_url)
            review_list =  data.get('reviewInfo',{}).get('reviewListInfo',{}).get('reviewList',[])
    if review_list:
        last_review = review_list[-1]
        add_time = dateutil.parser.parse(last_review['addTime'])+datetime.timedelta(hours=8)
        shop.第一条点评时间 = datetime.datetime.strftime(add_time,"%Y-%m-%d %H:%M:%S")
    else:
        shop.第一条点评时间 = None
    ShopMapper.update_shop_comment_time(shop=shop)
    # print(f">>>> after scrape: {shop}")
    time.sleep(random.randint(0,1))
    return True

def _request(url):
    # print(f"review url>> {url}")
    res=requests.get(url, headers={
        'User-Agent':   UserAgent().random
    },verify=False)
    print(res.text)
    data=res.json()
    return data

if __name__ == '__main__':
    get_dp_comment()