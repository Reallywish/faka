# coding:utf-8
import sys
import time

import requests
import simplejson as json
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

"""
100023038702 ipadPro12.9英寸 7399
100023038708 ipadPro11英寸 128G
100015068425 ipadmini8.3英寸 64G
"""

cookie = ""
skuIds = []


def lock(studentCode):
    try:
        skuId = skuIds.pop()
    except:
        logging.error("所有的skuId已经全部尝试，请更换账号！！！！！！！！！！！！！！！！！！！")
        sys.exit()
    url = "https://edu-web.jd.com/app/submit?xxwCheckCode={studentCode}&skuId={skuId}&shopId=1000000127&callback=jsonp_220d29794b25900".format(
        studentCode=studentCode, skuId=skuId)
    payload = {}
    headers = {
        'Host': 'edu-web.jd.com',
        'user-agent': 'jdapp;android;11.3.2;;;appBuild/98450;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1670424782021%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0(Linux;Android12;ONEPLUSA5010Build/SQ3A.220705.004;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/89.0.4389.72MQQBrowser/6.2TBS/046141MobileSafari/537.36',
        'accept': '*/*',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://edu-home.jd.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }
    response = requests.request("GET", url, headers=json.loads(json.dumps(headers)), data=payload).text
    # response = "s"
    logging.info(studentCode + "   验证结果========> " + str(response))
    if "账号申请次数已达上限" in response:
        logging.error("该账号认证次数超过限制，请更换账号重新锁码！！！！")
        input('按回车结束本程序！！！！！！！！')
    elif "申请失败，您的购买次数已达上限！" in response:
        logging.error("{code}  申请失败，您的购买次数已达上限！".format(code=studentCode))
        input("按回车结束本程序！！！！！！！！")
    else:
        lock(studentCode)


def getJdSkuId():
    url = "https://edu-web.jd.com/app/getSkuListByType?skuType=Ipad&shopId=1000000127&callback=jsonp_22696c2b2629da0"
    payload = {}
    headers = {
        'Host': 'edu-web.jd.com',
        'user-agent': 'jdapp;android;11.3.2;;;appBuild/98450;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1670424782021%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0(Linux;Android12;ONEPLUSA5010Build/SQ3A.220705.004;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/89.0.4389.72MQQBrowser/6.2TBS/046141MobileSafari/537.36',
        'accept': '*/*',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://edu-home.jd.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }

    try:
        response = requests.request("GET", url, headers=json.loads(json.dumps(headers)), data=payload).text
        jsonres = json.loads(response.replace("/**/jsonp_22696c2b2629da0(", "").replace(")", "").replace(";", ""))
        for skuSecondType in jsonres['data']:
            for sku in skuSecondType['skuList']:
                skuIds.append(str(sku['skuId']))

    except:
        logging.error("获取商品 skuId 时接口返回结果无法解析....请重新抓取cookie！！！！")
        input("按回车结束本程序！！！！！！！！")


if __name__ == '__main__':

    try:
        cookie = open("./cookie.ini", "r").readline()
        if cookie:
            logging.info("获取到的cookie ====> " + str(cookie))
        else:
            logging.error("未获取到cookie！！！！！！请在程序目录创建cookie.ini文件写入cookie即可！！！！")
            input('按回车结束本程序！！！！！！！！')

        getJdSkuId()
        if skuIds:
            logging.info("获取skuId成功 ====> " + str(skuIds))
            f = open("./code", "r")
            for l in f.readlines():
                code = l.replace("\n", "")
                lock(code)
        else:
            logging.error("获取skuId失败！！！！！检查cookie是否正确！！")
            input('按回车结束本程序！！！！！！！！')

    except:
        input('按回车结束本程序！！！！！！！！')
