#! -*- coding:utf-8 -*-
import time

from selenium import webdriver
import requests
import json


# 本地Chrome浏览器设置方法
# from selenium import webdriver
# import time
#
# chrome_driver = "./chromedriver.exe"
# driver = webdriver.Chrome(executable_path=chrome_driver)
# driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/')
# time.sleep(2)
#
# teacher = driver.find_element('teacher', '必须是吴枫呀')
# teacher.send_keys('必须是吴枫呀')
# assistant = driver.find_element('assistant')
# assistant.send_keys('都喜欢')
# time.sleep(1)
# button = driver.find_element('sub')
# time.sleep(1)
# button.click()
# time.sleep(1)
# driver.close()

def getP(csrftoken, cookie, level, champion_ids=[]):
    """
    5-1
    10-1
    12-2
    15-1
    16-1
    18-1
    20-1
    22-2
    24-1
    26-2
    28-1
    29-1
    :param csrftoken:
    :param cookie:
    :param level:
    :param champion_ids:
    :return:
    """
    url = "https://newsummoners.lol.garena.tw/api/prize-redemption/"

    payload = json.dumps({
        "level": level,
        "champion_ids": champion_ids
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'x-csrftoken': csrftoken,
        'referer': 'https://newsummoners.lol.garena.tw/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def start_(cookie, csrftoken):
    getP(csrftoken, cookie, 5, [1])
    getP(csrftoken, cookie, 10, [102])
    getP(csrftoken, cookie, 12, [16, 11])
    getP(csrftoken, cookie, 15, [18])
    getP(csrftoken, cookie, 16, [36])
    getP(csrftoken, cookie, 18, [37])
    getP(csrftoken, cookie, 20, [5])
    getP(csrftoken, cookie, 22, [51, 53])
    getP(csrftoken, cookie, 24, [54])
    getP(csrftoken, cookie, 26, [57, 81])
    getP(csrftoken, cookie, 28, [90])
    getP(csrftoken, cookie, 29, [99])


if __name__ == '__main__':
    start_(
        "sessionid=6yn1181xgxe73f4tko42fnfehb5c81o6; csrftoken=v1FdAJvIBnx1uplqjosFIBdApH02Wt6R52aq5ZwEmm6lWbaTBroNc89TTl2DbENG; _ga=GA1.2.411734966.1666075357; _gid=GA1.2.189220179.1666075357; _gat=1; _gat_gtag_UA_98198237_12=1",
        "v1FdAJvIBnx1uplqjosFIBdApH02Wt6R52aq5ZwEmm6lWbaTBroNc89TTl2DbENG")
