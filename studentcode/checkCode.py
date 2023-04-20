# coding:utf-8
import re

from tqdm import tqdm
from past.builtins import raw_input
import os

import configparser
import requests
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
    def __init__(self):

        self.auth = open("./auth.ini", "r", encoding='utf-8-sig').readline()
        self.proxy = None

    def getMaccheck(self, studentCode, status=0):
        # url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"
        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        payload = f"company_id=1&xxw_check_code={studentCode}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028"
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth.strip(),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html',
        }
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, proxies=self.proxy, data=payload, verify=False,
                                       timeout=10).json()
            if status == 1:
                if "True" in str(response):
                    # print(self.studentCode)
                    codeok.append(studentCode + "\r")
                else:
                    codeerr.append(studentCode + "\r")
            else:
                print(studentCode + "   结果：" + str(response))
            return True
        except:
            return False

    def getIpadcheck(self, studentCode, status=0):
        # url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"
        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        # payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
        #     code=self.studentCode)
        payload = f'company_id=1&xxw_check_code={studentCode}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'

        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth.strip(),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html',
        }

        session = requests.Session()
        session.trust_env = False
        try:
            response = session.request("POST", url, headers=headers, proxies=self.proxy, data=payload,
                                       timeout=10).json()
            # print(response)
            if status == 1:
                if "True" in str(response):
                    # print(self.studentCode)
                    codeok.append(studentCode + "\r")
                else:
                    codeerr.append(studentCode + "\r")
            elif status == 2:
                if "True" not in str(response):
                    print(studentCode)
            else:
                print(studentCode + "   结果：" + str(response))
            return True
        except Exception as e:
            # print(e)
            return False


class checkall:

    def __init__(self):
        self.auth = open("./auth.ini", "r", encoding='utf-8-sig').readline()
        self.proxy = None
        f = open('code_check.csv', 'w', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        c.writerow(['验证码', '平板', '电脑'])
        f.close()

    def getIpadAndMac(self, studentCode):
        # url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"
        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        payloadIpad = f'company_id=1&xxw_check_code={studentCode.strip()}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'
        payloadMac = f"company_id=1&xxw_check_code={studentCode.strip()}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028"

        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth.strip(),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html',
        }

        session = requests.Session()
        session.trust_env = False
        try:
            responseIpad = session.post(url, headers=headers, proxies=self.proxy, timeout=10,
                                        data=payloadIpad.encode('utf-8')).text
            # print(studentCode + "=====>" + responseIpad)
            responseMac = session.post(url, headers=headers, proxies=self.proxy, timeout=10,
                                       data=payloadMac.encode('utf-8')).text
            # print(studentCode + "=====>" + responseMac)

            if "true" in str(responseIpad).lower() and "true" in str(responseMac).lower():
                self.saveData([studentCode, "通过", "通过"])
            elif "true" not in str(responseIpad).lower() and "true" in str(responseMac).lower():
                self.saveData([studentCode, "不通过", "通过"])
            elif "true" in str(responseIpad).lower() and "true" not in str(responseMac).lower():
                self.saveData([studentCode, "通过", "不通过"])
            elif "很抱歉，由于您访问的URL有可能对网站造成安全威胁，您的访问被阻断。" in str(
                    responseIpad) or "很抱歉，由于您访问的URL有可能对网站造成安全威胁，您的访问被阻断。" in str(responseMac):
                return False
            else:
                self.saveData([studentCode, "不通过", "不通过"])
            return True
        except:
            return False

    def saveData(self, data):
        """
        数据存储
        """
        f = open('code_check.csv', 'a', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        print(" ".join(data))
        c.writerow(data)
        f.close()


class Spider():
    def __init__(self):
        f = open('tmp.csv', 'w', newline='', encoding='utf-8-sig')
        c = csv.writer(f)
        c.writerow(['验证码', '姓名', '学校', '在线验证码', '更新日期', '是否闭码'])
        f.close()

        self.df = open("./studentcode", "r", encoding='utf-8-sig')

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
        s = requests.session()
        s.keep_alive = False
        try:
            ret = s.request("GET", url, headers=headers, proxies=self.proxies, verify=False, timeout=10)
            # ret = requests.get(url, headers=headers, proxies=self.proxies, verify=False, timeout=10)
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
        ret = requests.get(proxy_url).json()
        print('代理接口返回的ip====>>>>>:', ret)
        if "白名单" in str(ret):
            ip_pattern = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
            ip = re.search(ip_pattern, ret['msg']).group(0)
            print("加入白名单ing。。。。" + ip)
            addwhite(ip)
    except:
        print("获取代理ip出错··")
        while True:
            try:
                ret = requests.get(proxy_url)
                print(ret)
                break
            except:
                print("获取代理ip循环内出错~！！！")
                continue

    try:
        while (ret['code'] != 200 and ret['code'] != 0):
            time.sleep(5)
            return changeProxies(proxy_url)
        data = ret['data'][0]
        proxies = {"https": f"{data['ip']}:{data['port']}"}
    except:
        data = ret.split(":")
        proxies = {"https": f"{data[0]}:{data[1]}"}
    return proxies


def get_public_ip():
    url = "https://api.ipify.org"
    try:
        response = requests.get(url)
        ip_address = response.text.strip()
        return ip_address
    except requests.RequestException as e:
        print("Error: ", e)
        return None


def addwhite(public_ip):
    """
    增加品易白名单
    :param public_ip:
    :return:
    """
    appkey = config.get("pinyi", "appkey")
    # 获取本机公网ip
    # public_ip = get_public_ip()
    url = f"https://pycn.yapi.3866866.com/index/index/save_white?neek={neek}&appkey={appkey}&white={public_ip}"
    response = requests.get(url).text
    print(response)


def startSchool(proxy_url):
    s = Spider()
    for code in s.df.readlines():
        if len(code.strip()) == 16:
            while s.getHtml(code.strip()):
                time.sleep(3)
                s.proxies = changeProxies(proxy_url)
    newdf = pandas.read_csv('tmp.csv')
    newdf.to_excel('result.xlsx', index=None)
    os.remove('tmp.csv')


def checkSchoolStart(proxy_url):
    configFile = "./proxy.ini"
    config = configparser.ConfigParser()

    if os.path.exists(configFile):
        config.read(configFile)

        """熊猫代理参数"""
        # secret = '0a669c9ff901cb72d4ad4e3438f1b036'
        # orderNo = 'GL20191206115727PPFPSsMm'
        # proxy_url = f'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret={secret}&orderNo={orderNo}&count=1&isTxt=0&proxyType=1'

        startSchool(proxy_url)
        input("执行完毕，请按回车结束···")



    else:
        config['elephant'] = {
            'appKey': '',
            'appSecret': ''
        }
        config['pinyi'] = {
            'neek': ''
        }
        with open('./proxy.ini', 'w', encoding='utf-8-sig') as cfg:
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
输入6检测Mac和Ipad，只将结果输出到控制
输入7将码学生信息解析（注意需要代理）,执行完毕会在本地生成一个result.xlsx
请按要求输入：=======>""")

        f = open("studentcode", "r", encoding='utf-8')
        configFile = "./proxy.ini"
        config = configparser.ConfigParser()
        if os.path.exists(configFile):
            proxy_tmp = raw_input(
                "使用品易代理请输入1，使用小象代理请输入2，请确保配置文件已添加相关配置！！！======>>")
            config.read(configFile)

            c = check()
            if proxy_tmp == "1":
                neek = config.get("pinyi", "neek")
                proxy_url = f'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek={neek}&type=2&sep=4&sb=&ip_si=1&mr=0'
            elif proxy_tmp == "2":
                appKey = config.get("elephant", "appkey")
                appSecret = config.get("elephant", "appSecret")
                proxy_url = f'https://api.xiaoxiangdaili.com/ip/get?appKey={appKey}&appSecret={appSecret}&cnt=&wt=json'
            else:
                proxy_url = "http://172.16.1.64:5555/random"
            if tmp == "1" or tmp == "2" or tmp == "5":

                for l in f.readlines():
                    code = l.strip()

                    if len(code) == 16:
                        if tmp == "1":
                            if proxy_url == None:
                                c.getIpadcheck(code)
                            else:
                                while not c.getIpadcheck(code):
                                    time.sleep(1)
                                    c.proxy = changeProxies(proxy_url)
                        elif tmp == "2":
                            # c.getMaccheck(code)
                            if proxy_url == None:
                                c.getMaccheck(code)
                            else:
                                while not c.getMaccheck(code):
                                    time.sleep(1)
                                    c.proxy = changeProxies(proxy_url)

            if tmp == "3" or tmp == "4":
                c = check()
                for l in tqdm(f.readlines()):
                    code = l.strip()
                    if tmp == "3":
                        if proxy_url == None:
                            c.getIpadcheck(code)
                        else:
                            while not c.getIpadcheck(code, 1):
                                time.sleep(1)
                                c.proxy = changeProxies(proxy_url)
                    elif tmp == "4":
                        if proxy_url == None:
                            c.getMaccheck(code)
                        else:
                            while not c.getMaccheck(code, 1):
                                time.sleep(1)
                                c.proxy = changeProxies(proxy_url)
                print("------------------不可用码------------------")
                for b in codeerr:
                    print(b)
                print("------------------可用码------------------")
                for a in codeok:
                    print(a)
            if tmp == '6':
                c = checkall()
                for l in tqdm(f.readlines()):
                    code = l.strip()

                    while not c.getIpadAndMac(code):
                        # time.sleep(1)
                        c.proxy = changeProxies(proxy_url)

            if tmp == '7':
                checkSchoolStart(proxy_url)
            input("按回车关闭。。。。")
        else:
            config['elephant'] = {
                'appKey': '',
                'appSecret': ''
            }
            config['pinyi'] = {
                'appkey': '',
                'neek': ''
            }
            with open('./proxy.ini', 'w') as cfg:
                config.write(cfg)
            print("配置文件已生成，请填入对应信息，重启该程序")
            input("回车结束~~~~")

    except Exception as e:
        print(e)
        input("按回车键关闭。。。")
