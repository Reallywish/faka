# coding:utf-8

import requests

"""
100023038702 ipadPro12.9英寸 7399
100023038708 ipadPro11英寸 128G
100015068425 ipadmini8.3英寸 64G
"""

cookie = "pt_key=app_openAAJjj-seADB6XzE6gOMp0BQwqgEC_Qr5LCcS8ZdcsZk5RwdrTH4W94967tZdLSiUI6dlBt_yJu0"


def lock(studentCode):
    url = "https://edu-web.jd.com/app/submit?xxwCheckCode={}&skuId=100015068425&shopId=1000000127&callback=jsonp_220d29794b25900".format(
        studentCode)
    payload = {}
    headers = {
        'Host': 'edu-web.jd.com',
        'user-agent': 'jdapp;android;11.3.2;;;appBuild/98450;ef/1;ep/%7B%22hdid%22%3A'
                      '%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1670376318741%2C%22ridx%22'
                      '%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D'
                      '%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D'
                      '%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong'
                      '.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010 '
                      'Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046141 Mobile Safari/537.36',
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
    response = requests.request("GET", url, headers=headers, data=payload)
    print(studentCode + " =====> " + str(response.text))


def getJdSkuId():
    url = "https://edu-web.jd.com/app/getSkuListByType?skuType=Ipad&shopId=1000000127&callback=jsonp_22696c2b2629da0"
    payload = {}
    headers = {
        'Host': 'edu-web.jd.com',
        'user-agent': 'jdapp;android;11.3.2;;;appBuild/98450;ef/1;ep/%7B%22hdid%22%3A'
                      '%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1670424782021%2C%22ridx%22'
                      '%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D'
                      '%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22CzS%3D%22%2C%22ud%22%3A%22YJK4ZwTrDQG3DNVwZtOzYm%3D%3D'
                      '%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong'
                      '.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010 '
                      'Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046141 Mobile Safari/537.36',
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

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    # f = open("./code", "r")
    # for l in f.readlines():
    #     code = l.replace("\n", "")
    #     lock(code)
    getJdSkuId()
