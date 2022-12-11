# coding:utf-8
import requests
from selenium import webdriver
from selenium import webdriver
import time
import simplejson as json
import proxyauth
import base64


def ip_affirm(proxies, testip1_url='http://httpbin.org/get?show_env=1'):  # requests查询实际的IP接口地址（代理）
    # 定义配置到的IP代理信息
    proxies = {"http": "http://" + proxies}
    try:
        response_get = requests.get(url=testip1_url, proxies=proxies)
        if response_get.status_code == 200:
            print(response_get.text)
            data = response_get.json()
            return data["origin"]
    except:
        print("#####Error: 查询IP连接出现异常，请检查IP代理账户密码及链接是否正确有效")
        input('点击回车键可退出......')
        exit()


def getIp():
    ipjson = requests.get("https://ip.jiangxianli.com/api/proxy_ip").json()
    print(ipjson)


def main():
    PROXY = "113.76.194.130:38662"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get('http://www.ip111.cn/')  # 在当前浏览器中访问百度
    js = 'window.open("https://1sq.cn/UVUgUJBY");'
    browser.execute_script(js)

    time.sleep(5000)


if __name__ == '__main__':
    main()
    # getIp()
