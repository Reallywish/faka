# coding:utf-8

import requests
from tqdm import tqdm
from past.builtins import raw_input
from checkSchool import checkSchoolStart

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
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, data=payload).json()
        except:
            response = "false"
        if status == 1:
            if "True" in str(response):
                # print(self.studentCode)
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        else:
            print(self.studentCode + "   结果：" + str(response))

    def getWatchCheck(self, status):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        payload = f'company_id=1&xxw_check_code={self.studentCode}&distributor_id=3337&edu_param=&items%5B0%5D%5Borigin_bn%5D=MNHW3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1448&items%5B0%5D%5Bitem_name%5D=Apple%20Watch%20Series%208%EF%BC%88GPS%2B%E8%9C%82%E7%AA%9D%E7%BD%91%E7%BB%9C%EF%BC%89%E9%93%9D%E9%87%91%E5%B1%9E%E8%A1%A8%E5%A3%B3%20-%20%E5%AD%A6%E7%94%9F%E9%99%90%E6%97%B6%E4%B8%93%E4%BA%AB&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1448'
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, data=payload).json()
        except:
            response = "false"
        if status == 1:
            if "True" in str(response):
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        else:
            print(self.studentCode + "   结果：" + str(response))

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

        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, data=payload).json()
        except:
            response = "false"
        if status == 1:
            if "True" in str(response):
                # print(self.studentCode)
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        elif status == 2:
            if "True" not in str(response):
                print(self.studentCode)
        else:
            print(self.studentCode + "   结果：" + str(response))


if __name__ == '__main__':

    try:
        tmp = raw_input(
            """检测ipad结果直接输出请输入1
检测mac结果直接输出请输入2
输入3将IPAD总结输出
输入4将MAC总结输出
输入5将手表总结输出
输入6将ipad和mac都检测
输入7将码学生信息解析（注意需要代理）,执行完毕会在本地生成一个result.xlsx
请按要求输入：=======>""")

        f = open("studentcode", "r")
        if tmp == "1" or tmp == "2" or tmp == "6":
            for l in f.readlines():
                code = l.strip()
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
                code = l.strip()
                if tmp == "3":
                    check(code).getIpadcheck(1)
                elif tmp == "4":
                    check(code).getMaccheck(1)
            print("------------------不可用码------------------")
            for b in codeerr:
                print(b)
            print("------------------可用码------------------")
            for a in codeok:
                print(a)
        if tmp == '5':
            for l in tqdm(f.readlines()):
                code = l.strip()
                check(code).getWatchCheck(1)
            print("------------------不可用码------------------")
            for b in codeerr:
                print(b)
            print("------------------可用码------------------")
            for a in codeok:
                print(a)
        if tmp == '7':
            checkSchoolStart()
        input("按回车关闭。。。。")
    except:
        input("按回车键关闭。。。")
