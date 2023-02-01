# coding:utf-8
import sys
import time

import requests
import simplejson as json
import logging
from past.builtins import raw_input

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

"""
100023038702 ipadPro12.9英寸 7399
100023038708 ipadPro11英寸 128G
100015068425 ipadmini8.3英寸 64G
"""

# skuIds = ["100019718287", "100034710084", "100019718259", "100034710060", "100019718261"]
lableLists = ["iPad Air", "iPad Pro", "iPad"]


def lock(studentCode, cookie, skuId):
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
    logging.info(studentCode + "使用 " + str(skuId) + "   验证结果========> " + str(response))
    if "账号申请次数已达上限" in response:
        logging.error("该账号认证次数超过限制，请更换账号重新锁码！！！！")
        input('按回车结束本程序！！！！！！！！')
    elif "申请失败，您的购买次数已达上限！" in response:
        logging.error("{code}  申请失败，您的购买次数已达上限！".format(code=studentCode))
        input("按回车结束本程序！！！！！！！！")
    elif "很遗憾本商品的申请次数已达上限" in response:
        logging.error("{code}  申请失败，您的购买次数已达上限！".format(code=studentCode))
        input("按回车结束本程序！！！！！！！！")
    # elif "结算年周期内认证成功次数已达上限" in response:

    elif "成功" in response:
        print("成功")
    else:
        lock(studentCode, cookie, skuId)


# def getJdSkuId():
#     try:
#         for lableList in lableLists:
#             url = "https://edu-web.jd.com/app/getSkuListByAttr?shopId=1000000127&skuType=Ipad&secondSkuType={}&attrListString=&areaListString=20%2C1715%2C43115%2C43155".format(
#                 lableList)
#             payload = {}
#             headers = {
#                 'Host': 'edu-web.jd.com',
#                 'user-agent': 'jdapp;android;11.4.0;;;appBuild/98605;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1674025894716%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010 Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36',
#                 'accept': '*/*',
#                 'x-requested-with': 'com.jingdong.app.mall',
#                 'sec-fetch-site': 'same-site',
#                 'sec-fetch-mode': 'no-cors',
#                 'sec-fetch-dest': 'script',
#                 'referer': 'https://edu-home.jd.com/',
#                 'accept-encoding': 'gzip, deflate',
#                 'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#                 'cookie': 'pt_key=app_openAAJjx5gEAEDFKQ3RsnsyFz6vDqKFSFDnm5oZNjhIt_sDLUmdiboYwXg81AmJKuEOkz09m1om7VO5TzgWIKA2llLjDgVJLvyO'
#             }
#             session = requests.Session()
#             session.trust_env = False
#             response = session.request("GET", url, headers=headers, data=payload)
#             for sku in response.json()["data"]["skuList"]:
#                 skuIds.append(sku["skuId"])
#
#
#     except:
#         logging.error("获取商品 skuId 时接口返回结果无法解析....请重新抓取cookie！！！！")
#         input("按回车结束本程序！！！！！！！！")


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
    print(response.text)


def get_record(status="check"):
    cookies = open("./cookie.ini", "r").readlines()
    for cookie in cookies:
        url = "https://edu-web.jd.com/app/myRecord?applyStatus=PASS&brand=apple"
        payload = {}
        headers = {
            'authority': 'edu-web.jd.com',
            'accept': '*/*',
            'accept-language': 'zh,zh-CN;q=0.9',
            'cookie': cookie.replace("\n", ""),
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
            # print(response.json())
            print(cookie.replace("\n", ""))
            for data in response["data"]:
                print("id: " + str(data["id"]) + "  名称：" + str(data["skuName"]) + "  学信码：" + str(
                    data["xxxCheckCode"]) + "  验证时间：" + str(data[
                                                                "startTime"]) + "  失效时间：" + str(data["endTime"]))
                if status != "check":
                    crearte_auth(int(data["id"]) - 1, cookie.replace("\n", ""))
        except:
            print(cookie.replace("\n", "") + "       EROOR!!!!  =====> 该cookie 可能已经失效！请验证")


def main():
    try:
        cookies = open("./cookie.ini", "r").readlines()
        if cookies:
            logging.info("获取到的cookie ====> " + str(cookies))
        else:
            logging.error("未获取到cookie！！！！！！请在程序目录创建cookie.ini文件写入cookie即可！！！！")
            input('按回车结束本程序！！！！！！！！')
        f = open("studentcode", "r").readlines()
        b = [f[i:i + 5] for i in range(0, len(f), 5)]

        # mac
        # skuIds = ["100009554947", "100016751652", "100009554935", "100029820099", "100029820113"]
        # ipad
        skuIds = ["100019718287", "100034710084", "100019718259", "100034710060", "100019718261"]

        for c in cookies:
            cookie = c.replace("\n", "")
            for skuId, code in zip(skuIds, b.pop(0)):
                lock(code.replace("\n", ""), cookie, skuId)
    except:
        input('按回车结束本程序！！！！！！！！')


if __name__ == '__main__':
    try:
        tmp = raw_input("输入1检测cookie是否有绑定，输入2 进行解绑，输入3进行锁码：===> ")
        if tmp == "1":
            get_record()
            input('按回车结束本程序！！！！！！！！')
        elif tmp == "2":
            get_record("2")
            input('按回车结束本程序！！！！！！！！')
        elif tmp == "3":
            main()
            input('按回车结束本程序！！！！！！！！')
        else:
            print("请按要求输入·····")
            input('按回车结束本程序！！！！！！！！')
    except:
        input("ERROR!!!!!!程序异常退出，请检查是否执行成功，按回车退出")
