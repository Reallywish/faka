# -*- coding:utf-8 -*-

import logging
import os
import random
import time

import configparser
import requests
import simplejson as json
from past.builtins import raw_input

# 本程序使用的是京东验证一次，使用小程序验证一次，验证单双。


# 双次码活动可用
doubleCode = []
# 单次码活动不可用
oneCode = []
# 坏码
badCode = []
# 锁码以后解不了的cookie
noLockCookie = []
# 超额码
excessCode = []

timeout = 10
auth = open("./auth.ini", "r", encoding="utf-8-sig").readline().strip()


def deStudentCode(cookie):
    """
    将锁了的码解开
    :param cookie:
    :return:
    """

    getidUrl = "https://edu-web.jd.com/app/myRecord?applyStatus=PASS&brand=apple"
    payload = {}
    headers = {
        'authority': 'edu-web.jd.com',
        'accept': '*/*',
        'accept-language': 'zh,zh-CN;q=0.9',
        'cookie': cookie,
        'referer': 'https://edu-home.jd.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    session = requests.Session()
    session.trust_env = False
    getIdResponse = session.request("GET", getidUrl, headers=headers, data=payload, timeout=timeout).json()
    id = getIdResponse["data"][0]['id'] - 1
    # id = 978042
    # 开始解锁
    decodeurl = "https://edu-web.jd.com/app/cancelAuth?applyRecordId={id}".format(id=id)
    payload = {}
    session = requests.Session()
    session.trust_env = False
    try:
        deCodeResponse = session.request("GET", decodeurl, headers=headers, data=payload, timeout=timeout).json()
    except:
        deCodeResponse = {'code': 400}
    if deCodeResponse['code'] == 0:
        return True
    else:
        return False


proxy = None


class check:

    def __init__(self, proxyurl):
        self.proxyurl = proxyurl

    def getIpadcheck(self, studentCode):
        """
        ipad 第9代
        :param studentCode:
        :return:
        """
        global proxy
        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        # payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
        #     code=studentCode)
        payload = f'company_id=1&xxw_check_code={studentCode.strip()}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'

        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': auth,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }

        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, data=payload, proxies=proxy,
                                       timeout=timeout).text

            if "很抱歉，由于您访问的URL有可能对网站造成安全威胁，您的访问被阻断。" in str(
                    response):
                proxy = self.changeProxies()
                return self.getIpadcheck(studentCode.strip())
            else:
                print(f"{studentCode.strip()}验证平板结果：{str(response)}")
                if "true" in str(response).lower():
                    return True
                else:
                    return False
        except Exception as e:
            proxy = self.changeProxies()
            return self.getIpadcheck(studentCode.strip())

    def changeProxies(self):
        """
        品易获取代理IP
        :param proxy_url:
        :return:
        """
        try:
            ret = requests.get(self.proxyurl)
            print('代理接口返回的ip====>>>>>:', ret.text)
        except:
            print("获取代理ip出错··")
            while True:
                try:
                    ret = requests.get(self.proxyurl)
                    print(ret)
                    break
                except:
                    print("获取代理ip循环内出错~！！！")
                    continue
        try:
            while (json.loads(ret.text)['code'] != 200 and json.loads(ret.text)['code'] != 0):
                time.sleep(1)
                return self.changeProxies()
            data = json.loads(ret.text)['data'][0]
            proxies = {"https": f"{data['ip']}:{data['port']}"}
        except:
            data = ret.text.split(":")
            proxies = {"https": f"{data[0]}:{data[1]}"}
        return proxies


def lock(studentCode, cookie, skuId="100019718287"):
    url = f"https://edu-web.jd.com/app/submit?xxwCheckCode={studentCode}&skuId={skuId}&shopId=1000000127&areaList=20%2C1715%2C43115%2C43155&callback=jsonp_1707b3fbf3a76b0".format(
        studentCode=studentCode, skuId=skuId)
    payload = {}
    headers = {
        'Host': 'edu-web.jd.com',
        'user-agent': 'jdapp;android;11.4.0;;;appBuild/98605;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1674036841881%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010 Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36',
        'accept': '*/*',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://edu-home.jd.com/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }
    session = requests.Session()
    session.trust_env = False
    response = session.request("GET", url, headers=json.loads(json.dumps(headers)), data=payload, timeout=timeout).text
    print(f"{studentCode}锁码验证结果========> {str(response)}")
    if "成功" in str(response):
        return "1"
    elif "redirect" in str(response) or "命中防刷逻辑" in str(response):
        return "2"
    elif "超时" in str(response):
        return "3"
    elif "很遗憾，学生信息验证未通过" in str(response):
        return "4"
    else:
        # 若失败，则说明是不爽
        return "0"


def main():
    cookies = open("./cookie.ini", "r", encoding="utf-8-sig").readlines()

    lines = open("studentcode", "r", encoding="utf-8-sig").readlines()
    configFile = "./proxy.ini"
    config = configparser.ConfigParser()
    if os.path.exists(configFile):
        proxy_tmp = raw_input(
            "使用品易代理请输入1，使用小象代理请输入2，请确保配置文件已添加相关配置！！！======>>")
        config.read(configFile)
        if proxy_tmp == "1":
            c = check(
                f'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek={config.get("pinyi", "neek")}&type=2&sep=4&sb=&ip_si=1&mr=0')
        elif proxy_tmp == "2":
            appKey = config.get("elephant", "appkey")
            appSecret = config.get("elephant", "appSecret")
            c = check(f'https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=json')
        for line, cookie in zip(lines, cookies):
            try:

                # 开始锁定
                lockRes = lock(line.strip(), cookie.strip())
                # 判断锁定结果：
                if lockRes == "2":
                    # # 如果有问题，则只将码重新加入，待再次判断
                    lines.append(line.strip())
                elif lockRes == "1":
                    # 如果结果是1的话，则说明活动可用，并且cookie也没问题。然后需要验证另一次是否有额度，再决定码是属于哪个组
                    # 调用测码，查询是否还有一次机会
                    checkIpadRes = c.getIpadcheck(line.strip())
                    if checkIpadRes:
                        # 如果返回true则说明还有一次额度，说明是双码
                        doubleCode.append(line.strip())
                    else:
                        # 如果返回不是true，则说明没有额度了。说明是单码
                        oneCode.append(line.strip())
                    # 最后解掉码
                    deCodeRes = deStudentCode(cookie.strip())
                    # 判断解码结果，如果返回成功，则将cookie重新加入cookie组，如果不成功，则标记不加入正常cookie组
                    if deCodeRes:
                        cookies.append(cookie.strip())
                    else:
                        # 加入未解开的cookie组
                        noLockCookie.append(cookie.strip())

                elif lockRes == "0":
                    # 则说明没有锁定成功，直接判定坏码
                    badCode.append(line.strip())

                elif lockRes == "3":
                    # 说明锁码没成功，需要进行重新检测。将码和cookie重新加入组即可。
                    cookies.append(cookie.strip())
                    lines.append(line.strip())
                elif lockRes == "4":
                    # 如果返回4 说明是 闭码
                    excessCode.append(line.strip())

            except:
                input("程序出错，请联系开发者！！！")

        print("--------------------------闭  码-------------------------------------")
        print("\r\n".join(excessCode))
        print("--------------------------超额码-------------------------------------")
        print("\r\n".join(badCode))
        print("--------------------------单次码-------------------------------")
        print("\r\n".join(oneCode))
        print("--------------------------双次码-------------------------------")
        print("\r\n".join(doubleCode))
        print("--------------------------未解锁cookie--------------------------------")
        print("\r\n".join(noLockCookie))

        input("运行结束，按回车关闭！！！")
    else:
        config['elephant'] = {
            'appKey': '',
            'appSecret': ''
        }
        config['pinyi'] = {
            'neek': ''
        }
        with open('./proxy.ini', 'w') as cfg:
            config.write(cfg)
        print("配置文件已生成，请填入对应信息，重启该程序")
        input("回车结束~~~~")

if __name__ == '__main__':
    # lines = open("studentcode", "r", encoding="utf-8-sig").readlines()
    #
    # for l in lines:
    #     c = check('http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek=65794&type=2&sep=4&sb=&ip_si=1&mr=0')
    #
    #     print(c.getIpadcheck(l))
    try:
        main()
    except Exception as e:
        print(e)
        input("错误退出！！！")
