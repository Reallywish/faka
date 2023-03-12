# -*- coding:utf-8 -*-
import sys
import time

import requests
import simplejson as json
import logging
import random

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

double = []
one = []
bad = []


def crearte_auth(id, cookie):
    url = "https://edu-web.jd.com/app/cancelAuth?applyRecordId={id}".format(id=id)
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
    response = session.request("GET", url, headers=headers, data=payload)
    print("解码：" + response.text)


def get_record(cookie, status="check"):
    # cookies = open("./cookie.ini", "r").readlines()
    url = "https://edu-web.jd.com/app/myRecord?applyStatus=PASS&brand=apple"
    payload = {}
    headers = {
        'authority': 'edu-web.jd.com',
        'accept': '*/*',
        'accept-language': 'zh,zh-CN;q=0.9',
        'cookie': cookie.strip(),
        'referer': 'https://edu-home.jd.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    try:
        session = requests.Session()
        session.trust_env = False
        response = session.request("GET", url, headers=headers, data=payload).json()
        print("获取码结果：" + str(response))
        for data in response["data"]:
            print("id: " + str(data["id"]) + "  名称：" + str(data["skuName"]) + "  学信码：" + str(
                data["xxxCheckCode"]) + "  验证时间：" + str(data[
                                                            "startTime"]) + "  失效时间：" + str(
                data["endTime"]))
            if status != "check":
                crearte_auth(int(data["id"]) - 1, cookie.strip())
    except:
        print(cookie.replace("\n", "") + "       EROOR!!!!  =====> 该cookie 可能已经失效！请验证")
        input("结束······")


def getIpadcheck(studentCode, auth):
    url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

    payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
        code=studentCode)
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
        response = session.request("POST", url, headers=headers, data=payload).json()
        print("验证平板结果：" + str(response))
    except:
        response = "false"

    if "True" in str(response):
        # print(self.studentCode)
        one.append(studentCode)
    else:
        bad.append(studentCode)


def lock(studentCode, cookie, auth, skuId="100019718287"):
    url = f"https://edu-web.jd.com/app/submit?xxwCheckCode={studentCode}&skuId={skuId}&shopId=1000000127&areaList=20%2C1715%2C43115%2C43155&callback=jsonp_1707b3fbf3a76b0".format(
        studentCode=studentCode, skuId=skuId)
    print(url)
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
    response = session.request("GET", url, headers=json.loads(json.dumps(headers)), data=payload).text
    # response = "s"
    print("锁码验证结果========> " + str(response))
    if "成功" in str(response):
        # 若成功，则解，说明是爽
        time.sleep(1)
        get_record(cookie, "1")
        double.append(studentCode)
        return True
    elif "redirect" in str(response) or "命中防刷逻辑" in str(response):
        print("这块返回了false" + str(response))
        return False
    elif "超时" in str(response):
        lock(studentCode, cookie, auth, skuId)
    else:
        # 若失败，则说明是不爽
        getIpadcheck(studentCode, auth)
        return True


if __name__ == '__main__':
    auth = open("./auth.ini", "r").readline().strip()
    cookies = open("./cookie.ini", "r").readlines()

    lines = open("studentcode", "r").readlines()
    for line, cookie in zip(lines, cookies):
        try:
            print(line.strip(), cookie.strip())
            suiji = random.randint(1, 5)
            print(f"开始随机延迟，本次延迟{suiji}秒，否则担心触碰防刷~~~~")
            time.sleep(suiji)
            # print(line.strip())
            if not lock(line.strip(), cookie.strip(), auth):
                print("cookie 可能有问题···")
                break
            else:
                print("无问题")
            cookies.append(cookie)
        except:
            print("出问题了！")
    print("--------------------------双次码-----------------------------")
    print("\r\n".join(double))
    print("--------------------------单次码-----------------------------")
    print("\r\n".join(one))
    print("--------------------------坏  码-----------------------------")
    print("\r\n".join(bad))
