#! -*- coding:utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import simplejson as json

from Garena.getprize import start_

option = ChromeOptions()

option.add_argument("--user-data-dir=" + r"C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/")

option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--no-sandbox")
option.add_argument("--lang=zh-CN")

browser = webdriver.Chrome(options=option)

browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

browser.get(
    'https://auth.garena.com/oauth/login?redirect_uri=https%3A%2F%2Fnewsummoners.lol.garena.tw%2Fgarena_oauth%2Flogin%2Fcallback%2F&client_id=200032&response_type=token&locale=zh-TW')
time.sleep(20)
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
