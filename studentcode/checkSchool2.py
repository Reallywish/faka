# coding=utf-8
import requests
import json
import time
from bs4 import BeautifulSoup
import pandas
import csv


# def changeProxies(proxy_url):
#     """
#     熊猫获取代理IP
#     :param proxy_url:
#     :return:
#     """
#     ret = requests.get(proxy_url)
#     while json.loads(ret.text)['code'] != "0":
#         print(ret.text)
#         time.sleep(1)
#         return changeProxies(proxy_url)
#     data = json.loads(ret.text)["obj"][0]
#     proxies = {"http": f"http://{data['ip']}:{data['port']}","https": f"https://{data['ip']}:{data['port']}"}
#     print('--->代理IP:', ret.text)
#     return proxies


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
    while json.loads(ret.text)['code'] != 200:
        time.sleep(1)
        return changeProxies(proxy_url)
    data = json.loads(ret.text)['data'][0]
    proxies = {"https": f"{data['ip']}:{data['port']}"}
    print('--->代理IP:', ret.text)
    return proxies


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
        except:
            return True
        if '继续' in ret.text:
            return True
        if '在线验证报告已过期，无法在线验证。' in ret.text:
            self.saveData([code, '', '', '', '闭码'])
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
        print(data)
        c.writerow(data)
        f.close()


if __name__ == '__main__':
    s = Spider()
    """熊猫代理参数"""
    # secret = '0a669c9ff901cb72d4ad4e3438f1b036'
    # orderNo = 'GL20191206115727PPFPSsMm'
    # proxy_url = f'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret={secret}&orderNo={orderNo}&count=1&isTxt=0&proxyType=1'

    """品易代理参数"""
    # neek = '65794'
    # proxy_url = f'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek={neek}&type=2&sep=4&sb=&ip_si=1&mr=0'
    # 小象代理
    proxy_url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=949648503121268736&appSecret=jPYNMXeM&cnt=&wt=json'
    for code in s.df.readlines():
        while s.getHtml(code.strip()):
            time.sleep(3)
            s.proxies = changeProxies(proxy_url)
    newdf = pandas.read_csv('tmp.csv')
    newdf.to_excel('结果.xlsx', index=None)
