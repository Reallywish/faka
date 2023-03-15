# -*- coding:utf-8 -*-
import os

import requests
from tqdm import tqdm

codeok = []
codeerr = []


class check:
    def __init__(self, studentCode):
        self.studentCode = studentCode
        self.auth = open("./auth.ini", "r").readline()

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


if __name__ == '__main__':
    try:
        f = open("./studencode.txt", "r")
        for l in tqdm(f.readlines()):
            check(l.strip()).getIpadHotcheck(1)
        print("------------------不可用码------------------")
        for b in codeerr:
            print(b)
        print("------------------可用码------------------")
        for a in codeok:
            print(a)
        input("运行结束，请选中以后右键直接复制对应内容即可！！")
    except FileNotFoundError as e:
        with open('./studencode.txt', 'w') as fp:
            pass
        input("警告：未发现存码文件，已创建，请将码放入文件内再次运行该程序！！！！！ 回车结束！！！！")
    except:
        input("ERROR!!!!!!程序出错，请联系开发者！！！！！")






