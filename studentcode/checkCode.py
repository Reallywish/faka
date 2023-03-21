# coding:utf-8

import requests
from tqdm import tqdm
from past.builtins import raw_input
import os

import configparser
import requests
import json
import time
from bs4 import BeautifulSoup
import pandas
import csv
import urllib3

urllib3.disable_warnings()

"""
平板msn：MHQR3CH/A
平板good_ids: 756

电脑msn：MLY33CH/A
电脑good_ids:1028
"""

codeok = []
codeerr = []
codeMac = []
codeIpad = []


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
            print(response)
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

        # payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
        #     code=self.studentCode)
        payload = f'company_id=1&xxw_check_code={self.studentCode}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'

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

    def getIpadAndMac(self, status='0'):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        if status == '1':
            payloadIpad = f'company_id=1&xxw_check_code={self.studentCode}&distributor_id=2754&edu_param=FY23Q2Q3M4MProgram&items%5B0%5D%5Borigin_bn%5D=MNXD3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1381&items%5B0%5D%5Bitem_name%5D=iPad%20Pro%2011%20%E8%8B%B1%E5%AF%B8%EF%BC%88%E6%96%B0%E6%AC%BE%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1381'
            payloadMac = f'company_id=1&xxw_check_code={self.studentCode}&distributor_id=3539&edu_param=FY23Q2Q3M4MProgram&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20(M2)&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028'
        else:
            payloadIpad = f'company_id=1&xxw_check_code={self.studentCode.strip()}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'
            payloadMac = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028".format(
                code=self.studentCode.strip())

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
            responseIpad = session.request("POST", url, headers=headers, data=payloadIpad).json()
            responseMac = session.request("POST", url, headers=headers, data=payloadMac).json()
            # print(responseIpad)
            # print(responseMac)
        except:
            responseIpad = "false"
            responseMac = "false"

        if "True" in str(responseIpad) and "True" in str(responseMac):
            codeok.append(self.studentCode.strip())
        elif "True" not in str(responseIpad) and "True" in str(responseMac):
            codeMac.append(self.studentCode.strip())
        elif "True" in str(responseIpad) and "True" not in str(responseMac):
            codeIpad.append(self.studentCode.strip())
        else:
            codeerr.append(self.studentCode.strip())

    def getIpadHotcheck(self, status=0):

        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        payload = f'company_id=1&xxw_check_code={self.studentCode}&distributor_id=2754&edu_param=FY23Q2Q3M4MProgram&items%5B0%5D%5Borigin_bn%5D=MNXD3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1381&items%5B0%5D%5Bitem_name%5D=iPad%20Pro%2011%20%E8%8B%B1%E5%AF%B8%EF%BC%88%E6%96%B0%E6%AC%BE%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1381'
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Connection': 'keep-alive',
            'Content-Length': '353',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQyNTAxMDBfZXNwaWVyX29adEdONU1yWTR3d1BVTWotTXFjcW9WM284OG9fZXNwaWVyX29adEdONU1yWTR3d1BVTWotTXFjcW9WM284OG8iLCJzdWIiOiI0MjUwMTAwX2VzcGllcl9vWnRHTjVNclk0d3dQVU1qLU1xY3FvVjNvODhvX2VzcGllcl9vWnRHTjVNclk0d3dQVU1qLU1xY3FvVjNvODhvIiwidXNlcl9pZCI6NDI1MDEwMCwiZGlzYWJsZWQiOjAsImNvbXBhbnlfaWQiOiIxIiwid3hhcHBfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ3b2FfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ1bmlvbmlkIjoib1p0R041TXJZNHd3UFVNai1NcWNxb1Yzbzg4byIsIm9wZW5pZCI6Im9adEdONU1yWTR3d1BVTWotTXFjcW9WM284OG8iLCJhdXRob3JpemVyX2FwcGlkIjoid3hkMjY3OGM0MzBiZmQzYWJjIiwib3BlcmF0b3JfdHlwZSI6InVzZXIifQ.p7oz79OTmo0q_H33tY9jD8_3KiH29CcaqU3lgKqS6VE',
            'charset': 'utf-8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ONEPLUS A5010 Build/SQ3A.220705.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5015 MMWEBSDK/20221206 MMWEBID/1054 MicroMessenger/8.0.32.2300(0x28002035) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/x-www-form-urlencoded',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/91/page-frame.html',
            'Cookie': 'acw_tc=276077a216785479397647532e5a082ec824a6562a8856e03dd54e921e1a1d'
        }

        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, data=payload).text
        except:
            response = "false"
        if status == 1:
            if "true" in str(response):
                # print(self.studentCode)
                codeok.append(self.studentCode + "\r")
            else:
                codeerr.append(self.studentCode + "\r")
        elif status == 2:
            if "true" not in str(response):
                print(self.studentCode)
        else:
            print(self.studentCode + "   结果：" + str(response))


class Spider():
    def __init__(self):
        f = open('tmp.csv', 'w', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        c.writerow(['验证码', '姓名', '学校', '在线验证码', '更新日期', '是否闭码'])
        f.close()

        self.df = open("./studentcode", "r")

        self.proxies = None

    def getHtml(self, code):
        """
        获取数据
        如果出现验证码，就需要重试，这个函数会返回True，代表需要切换代理，进行重试
        如果获取正常，就会自动进行数据的存储
        """
        url = f'https://www.chsi.com.cn/xlcx/bg.do?vcode={code}&srcid=bgcx'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        try:
            ret = requests.get(url, headers=headers, proxies=self.proxies, verify=False, timeout=10)
        except Exception as err:
            print(err)
            return True
        if '继续' in ret.text:
            return True
        if '在线验证报告已过期，无法在线验证。' in ret.text:
            self.saveData([code, '', '', '', '', '闭码'])
            return False
        if '在线验证报告已关闭，无法在线验证。' in ret.text:
            self.saveData([code, '', '', '', '', '闭码'])
            return False
        soup = BeautifulSoup(ret.text, 'html.parser')
        try:
            update_time = soup.find('div', class_='update-time').get_text().replace('更新日期：', '')
        except:
            update_time = ''
        school = ''
        try:
            lineCode = soup.find('span', class_='yzm').get_text()  # 在线验证码
        except:
            lineCode = ''
        try:
            tmpList = soup.find_all('div', class_='report-info-item')
            for tmp in tmpList:
                if tmp.find('div', class_='label').get_text() == '院校':
                    school = tmp.find('div', class_='value long').get_text()  # 提取院校
                    break
        except:
            school = ''
        studenName = ''
        try:
            tmpList = soup.find_all('div', class_='report-info-item')
            for tmp in tmpList:
                if tmp.find('div', class_='label').get_text() == '姓名':
                    studenName = tmp.find('div', class_='value').get_text()  # 提取院校
                    break
        except:
            studenName = ''
        self.saveData([code, studenName, school, lineCode, update_time, '非闭码'])
        return False

    def saveData(self, data):
        """
        数据存储
        """
        f = open('tmp.csv', 'a', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        print(" ".join(data))
        c.writerow(data)
        f.close()


def changeProxies(proxy_url):
    """
    品易获取代理IP
    :param proxy_url:
    :return:
    """
    try:
        ret = requests.get(proxy_url)
        print('代理接口返回的ip====>>>>>:', ret.text)
    except:
        while True:
            try:
                ret = requests.get(proxy_url)
                print(ret)
                break
            except:
                continue
    while (json.loads(ret.text)['code'] != 200 and json.loads(ret.text)['code'] != 0):
        time.sleep(1)
        return changeProxies(proxy_url)
    data = json.loads(ret.text)['data'][0]
    proxies = {"https": f"{data['ip']}:{data['port']}"}
    return proxies


def start(proxy_url):
    s = Spider()
    for code in s.df.readlines():
        while s.getHtml(code.strip()):
            time.sleep(3)
            s.proxies = changeProxies(proxy_url)
    newdf = pandas.read_csv('tmp.csv')
    newdf.to_excel('result.xlsx', index=None)
    os.remove('tmp.csv')


def checkSchoolStart():
    configFile = "./school.ini"
    config = configparser.ConfigParser()

    if os.path.exists(configFile):
        status = raw_input(
            "使用品易代理请输入1，使用小象代理请输入2，请确保配置文件已添加相关配置！！！======>>")
        config.read(configFile)

        """熊猫代理参数"""
        # secret = '0a669c9ff901cb72d4ad4e3438f1b036'
        # orderNo = 'GL20191206115727PPFPSsMm'
        # proxy_url = f'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret={secret}&orderNo={orderNo}&count=1&isTxt=0&proxyType=1'

        if status == "1":
            """品易代理参数"""
            neek = config.get("pinyi", "neek")
            proxy_url = f'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek={neek}&type=2&sep=4&sb=&ip_si=1&mr=0'
            start(proxy_url)
            input("执行完毕，请按回车结束···")
        elif status == "2":
            """小象代理参数"""
            appKey = config.get("elephant", "appkey")
            appSecret = config.get("elephant", "appSecret")
            proxy_url = f'https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=json'
            start(proxy_url)
            input("执行完毕，请按回车结束···")
        else:
            input("请按要求输入！！！")


    else:
        config['elephant'] = {
            'appKey': '',
            'appSecret': ''
        }
        config['pinyi'] = {
            'neek': ''
        }
        with open('./school.ini', 'w') as cfg:
            config.write(cfg)
        print("配置文件已生成，请填入对应信息，重启该程序")
        # input("回车结束~~~~")


if __name__ == '__main__':

    try:
        tmp = raw_input(
            """检测ipad结果直接输出请输入1
检测mac结果直接输出请输入2
输入3将IPAD总结输出
输入4将MAC总结输出
输入5检测Mac和Ipad，结果输出到控制台
输入6检测Mac和Ipad，只将结果输出到控制
输入7将活动码每个结果输出到控制台
输入8将活动码批量检测结果输出到控制台(只检测平板）
输入9将活动码和电脑活动码检测结果输出到控制台
输入10将码学生信息解析（注意需要代理）,执行完毕会在本地生成一个result.xlsx
请按要求输入：=======>""")

        f = open("studentcode", "r")
        if tmp == "1" or tmp == "2" or tmp == "5":
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
        if tmp == '6':
            for l in tqdm(f.readlines()):
                code = l.strip()
                check(code).getIpadAndMac()

            print("------------------全部都不可用码------------------")
            for b in codeerr:
                print(b)
            print("------------------只有电脑可用码------------------")
            for d in codeMac:
                print(d)
            print("------------------只有平板可用码------------------")
            for a in codeIpad:
                print(a)
            print("--------------------全部可用码-------------------")
            for c in codeok:
                print(c)

        if tmp == '7':
            for l in f.readlines():
                check(l.strip()).getIpadHotcheck()
        if tmp == '8':
            for l in tqdm(f.readlines()):
                check(l.strip()).getIpadHotcheck(1)
            print("------------------不可用码------------------")
            for b in codeerr:
                print(b)
            print("------------------可用码------------------")
            for a in codeok:
                print(a)
        if tmp == "9":
            for l in tqdm(f.readlines()):
                code = l.strip()
                check(code).getIpadAndMac("1")

            print("------------------全部都不可用码------------------")
            for b in codeerr:
                print(b)
            print("------------------只有电脑可用码------------------")
            for d in codeMac:
                print(d)
            print("------------------只有平板可用码------------------")
            for a in codeIpad:
                print(a)
            print("--------------------全部可用码-------------------")
            for c in codeok:
                print(c)
        if tmp == '10':
            checkSchoolStart()

        input("按回车关闭。。。。")
    except:
        input("按回车键关闭。。。")
