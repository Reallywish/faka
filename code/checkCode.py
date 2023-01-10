# coding:utf-8

import requests
from tqdm import tqdm
from past.builtins import raw_input

"""
平板msn：MHQR3CH/A
平板good_ids: 756

电脑msn：MLY33CH/A
电脑good_ids:1028
"""

codeok = []
codeerr = []


class check:
    def __init__(self, studentCode):
        self.studentCode = studentCode
        self.auth = open("./auth.ini", "r").readline()

    def getMaccheck(self, status=0):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028".format(
            code=self.studentCode)
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if status == 1:
            if "true" in str(response.text):
                # print(self.studentCode)
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        else:
            print(self.studentCode + "   结果：" + str(response.json()))

    def getIpadcheck(self, status=0):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
            code=self.studentCode)
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if status == 1:
            if "true" in str(response.text):
                # print(self.studentCode)
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        elif status == 2:
            if "true" not in str(response.text):
                print(self.studentCode)
        else:
            print(self.studentCode + "   结果：" + str(response.json()))


if __name__ == '__main__':

    try:
        tmp = raw_input("检测ipad请输入1，检测mac请输入2，输入3将IPAD总结输出，输入4将MAC总结输出。如果ipad和mac都检测请输入5:===> ")

        f = open("./code", "r")
        if tmp == "1" or tmp == "2" or tmp == "5":
            for l in f.readlines():
                code = l.replace("\n", "")
                if tmp == "1":
                    check(code).getIpadcheck()
                elif tmp == "2":
                    check(code).getMaccheck()
                else:
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    check(code).getIpadcheck()
                    check(code).getMaccheck()

        if tmp == "3" or tmp == "4":
            for l in tqdm(f.readlines()):
                code = l.replace("\n", "")
                if tmp == "3":
                    check(code).getIpadcheck(1)
                elif tmp == "4":
                    check(code).getMaccheck(1)
            print("------------------可用码------------------")
            for a in codeok:
                print(a)
            print("------------------不可用码------------------")
            for b in codeerr:
                print(b)

        input("按回车关闭。。。。")
    except:
        input("按回车键关闭。。。")
