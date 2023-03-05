# -*- coding:utf-8 -*-
import json

from lxml import etree
import browser_cookie3
from selenium import webdriver
import time
import webbrowser
import os
import requests
import winreg
import zipfile
from selenium.webdriver import ChromeOptions

url = 'http://npm.taobao.org/mirrors/chromedriver/'


# chromedriver download link
def get_Chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    return version


def get_server_chrome_versions():
    '''return all versions list'''
    versionList = []
    url = "https://registry.npmmirror.com/-/binary/chromedriver/"
    rep = requests.get(url).json()
    for item in rep:
        versionList.append(item["name"])
    return versionList


def download_driver(download_url):
    '''下载文件'''
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('下载成功')


def get_version(file_path):
    '''查询系统内的Chromedriver版本'''
    outstd2 = os.popen(file_path + 'chromedriver --version').read()
    return outstd2.split(' ')[1]


def unzip_driver(path):
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip", 'r')
    for file in f.namelist():
        f.extract(file, path)


def check_update_chromedriver(file_path):
    chromeVersion = get_Chrome_version()
    chrome_main_version = int(chromeVersion.split(".")[0])  # chrome主版本号
    driver_main_version = ''
    if os.path.exists(os.path.join(file_path, "chromedriver.exe")):
        driverVersion = get_version(file_path)
        driver_main_version = int(driverVersion.split(".")[0])  # chromedriver主版本号
    download_url = ""
    if driver_main_version != chrome_main_version:
        print("chromedriver版本与chrome浏览器不兼容，更新中>>>")
        versionList = get_server_chrome_versions()
        if chromeVersion in versionList:
            download_url = f"{url}{chromeVersion}/chromedriver_win32.zip"
        else:
            for version in versionList:
                if version.startswith(str(chrome_main_version)):
                    download_url = f"{url}{version}/chromedriver_win32.zip"
                    break
            if download_url == "":
                print("暂无法找到与chrome兼容的chromedriver版本，请在http://npm.taobao.org/mirrors/chromedriver/ 核实。")

        download_driver(download_url=download_url)
        path = file_path
        unzip_driver(path)
        os.remove("chromedriver.zip")
        print('更新后的Chromedriver版本为：', get_version(file_path))
    else:
        print("chromedriver版本与chrome浏览器相兼容，无需更新chromedriver版本！")
    return os.path.join(file_path, "chromedriver.exe")


def submitCode(code, cook, proxy):
    try:
        url = "https://www.chsi.com.cn/xlcx/bg.do?vcode={}&srcid=bgcx".format(code)
        payload = 'validationCode=AFDRN8J6M1PEZXMJ'
        headers = {
            'Host': 'www.chsi.com.cn',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www.chsi.com.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.chsi.com.cn/wap/report/search.jsp',
            'Accept-Language': 'zh,zh-CN;q=0.9',
            'Cookie': cook
        }
        # proxies = {"https", "223.247.46.104:8089"}
        response = requests.request("POST", url, headers=headers, proxies=proxy, data=payload).text
        return response
    except:
        return ""


def main():
    webbrowser.open("https://www.chsi.com.cn/xlcx/bgcx.jsp")
    time.sleep(5)
    cookies = browser_cookie3.chrome()
    a = ""
    for c in cookies:
        if "chsi.com" in str(c):
            a += (c.name + "=" + c.value + "; ")
    print(a)
    submitCode("AHQJTWDH5EUE8SSQ", a)
    # 关闭IE浏览器
    os.system('taskkill /F /IM chrome.exe')


def analyze_html(html):
    try:
        html = etree.HTML(html, etree.HTMLParser(encoding="utf-8"))

        resright = html.xpath('//div[@class="col-right"]/text()')
        if len(resright) != 0:
            return ("\t".join(resright))
        else:
            return ""
    except:
        return ""


def changeProxies(proxy_url):
    """
    品易获取代理IP
    :param proxy_url:
    :return:
    """
    try:
        ret = requests.get(proxy_url)
    except:
        while True:
            try:
                ret = requests.get(proxy_url)
                break
            except:
                continue
    while json.loads(ret.text)['code'] != 0:
        print(ret.text)
        time.sleep(1)
        return changeProxies(proxy_url)
    data = json.loads(ret.text)['data'][0]
    proxies = {"http": f"http://{data['ip']}:{data['port']}", "https": f"https://{data['ip']}:{data['port']}"}
    print('--->代理IP:', ret.text)
    return proxies


if __name__ == "__main__":
    f = open("studentcode", "r")
    for l in f.readlines():
        try:
            neek = '65794'
            proxy_url = f'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek={neek}&type=2&sep=4&sb=&ip_si=1&mr=0'
            proxy = changeProxies(proxy_url)
            web_url = "https://www.chsi.com.cn/xlcx/bgcx.jsp"
            options = ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_argument("-headless")
            options.add_argument('--disable-blink-features=AutomationControlled')

            with open('./stealth.min.js') as f:
                js = f.read()

            browser = webdriver.Chrome(executable_path=".\\chromedriver.exe", chrome_options=options)
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })
            # 打开网页
            browser.get(web_url)
            time.sleep(3)
            cookies = browser.get_cookies()
            a = ""
            for c in cookies:
                if "chsi.com" in str(c):
                    a += (c['name'] + "=" + c['value'] + "; ")
            reshtml = submitCode(l.strip(), a, proxy)
            # print(reshtml)
            if reshtml:
                # print("开始解析查询结果：")
                result = analyze_html(reshtml)
                if result != "":
                    print(result)
                else:
                    print(l.strip() + "： 检测出错,可能是闭码~~~~~")
            else:
                print(l.strip() + "： 提交出错,可能ip多次提交导致出验证码，请更换ip~~~~~")
        except:
            print(l.strip() + "： 整体出错,请联系开发人员····")
