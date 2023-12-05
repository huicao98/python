import time
from ..selenium_utils import build_driver

driver = build_driver()
driver.get("https://www.baidu.com")

time.sleep(100)