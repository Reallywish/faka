#! -*- coding:utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import simplejson as json

from Garena.getprize import start_

# option = ChromeOptions()
# C:\Users\Administrator\AppData\Local\Google\Chrome\User Data
# option.add_argument("--user-data-dir=" + r"C:/Users/15986/AppData/Local/Google/Chrome/User Data")

# option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_argument("--no-sandbox")
# option.add_argument("--lang=zh-CN")

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

browser = webdriver.Firefox(executable_path=r"E:\python\faka\Garena\geckodriver.exe",
                            firefox_binary=r"C:\Program Files\Mozilla Firefox\firefox.exe",
                            options=options)






# browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
browser.implicitly_wait(10)

browser.get(
    'https://newsummoners.lol.garena.tw')
time.sleep(2000)
cookies = browser.get_cookies()
c = []
csrftoken = ""
for cookie in cookies:
    c.append(cookie.get("name") + "=" + cookie.get("value"))
    if "csrftoken" in str(cookie):
        csrftoken = cookie.get("value")

print("获取cookie成功：" + ";".join(c))
print("token为：" + str(csrftoken))

start_(";".join(c), csrftoken)

# print(browser.find_element("input","Garena 帳號，電子信箱或手機號碼"))
browser.close()
