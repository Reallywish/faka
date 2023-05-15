# -*- coding:utf-8 -*-
import configparser
import multiprocessing
import re
import sys
import time
from multiprocessing import Pool, Manager

import requests
from past.builtins import raw_input
from tqdm import tqdm


def addwhite(public_ip, appkey):
    """
    增加品易白名单
    :param public_ip:
    :return:
    """
    # 获取本机公网ip
    # public_ip = get_public_ip()
    url = f"https://pycn.yapi.py.cn/index/index/save_white?neek={neek}&appkey={appkey}&white={public_ip}"
    response = requests.get(url).text
    print(response)


def getIpadcheck(studentCode, auth, status, proxyArr, codeOk, codeErr):
    url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

    if status == "1":
        # 平板参数
        payload = f'company_id=1&xxw_check_code={studentCode}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'
    else:
        # 电脑参数
        payload = f"company_id=1&xxw_check_code={studentCode}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028"
    headers = {
        'Host': 'aar-orderapi.tjtjshengtu.com',
        'Authorization': auth,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'authorizer-appid': 'wxd2678c430bfd3abc',
        'content-type': 'application/x-www-form-urlencoded',
        'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html',
    }

    try:
        session = requests.Session()
        session.trust_env = False
        response = session.request("POST", url, headers=headers, proxies=proxyArr.pop(), data=payload,
                                   timeout=10).text
        # print(studentCode + "  结果：" + response)
        if "true" in str(response).lower():
            codeOk.append(studentCode)
        elif "很抱歉，由于您访问的URL有可能对网站造成安全威胁，您的访问被阻断。" in str(response):
            getIpadcheck(studentCode, auth, status, proxyArr, codeOk, codeErr)
        else:
            codeErr.append(studentCode)
    except Exception as e:
        # 如果报错，说明代理可能不可用，则更换代理 重新发起请求
        # print(f"{studentCode} 出错重试====>{e}")
        # print(proxyArr)
        getIpadcheck(studentCode, auth, status, proxyArr, codeOk, codeErr)


def changeProxies(neek, appkey, mylist, count=200):
    """
    小象、品易获取代理IP
    :param proxy_url:
    :return:
    """
    global ret
    proxyurl = f"http://tiqu.pyhttp.taolop.com/getflowip?count={count}&neek={neek}&type=2&sep=4&sb=&ip_si=1&mr=0"
    try:
        ret = requests.get(proxyurl).json()
        if "白名单" in str(ret):
            ip_pattern = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
            ip = re.search(ip_pattern, ret['msg']).group(0)
            print("加入白名单ing。。。。" + ip)
            addwhite(ip, appkey)
            ret = requests.get(proxyurl).json()
    except Exception as e:
        while True:
            try:
                ret = requests.get(proxyurl)
                break
            except:
                continue
    while (ret['code'] != 200 and ret['code'] != 0):
        time.sleep(2)
        changeProxies(count, neek, mylist)
    for ip in ret['data']:
        proxies = {"https": f"{ip['ip']}:{ip['port']}"}
        mylist.append(proxies)


def proxy_add(my_list, neek, appkey):
    # print("woshi proxy add")
    while True:
        time.sleep(1)
        if len(my_list) < 100:
            # print("补充ip")
            changeProxies(neek, appkey, my_list)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    try:
        tmp = raw_input(
            """检测ipad结果直接输出请输入1
检测mac结果直接输出请输入2
请按要求输入：=======>""")
        configFile = "./proxy.ini"
        config = configparser.ConfigParser()
        config.read(configFile,encoding="utf-8-sig")
        neek = config.get("pinyi", "neek")
        appkey = config.get("pinyi", "appkey")

        # 定义了进程中共享使用的几个数组。
        manager = Manager()
        my_list = manager.list()
        codeOk = manager.list()
        codeErr = manager.list()

        changeProxies(neek, appkey, my_list)
        # print(my_list)
        p = Pool(int(config.get("pool", "count")))
        auth = open("./auth.ini", "r", encoding='utf-8-sig').readline().strip()
        f = open("studentcode", "r", encoding='utf-8').readlines()
        pbar = tqdm(total=len(f), position=0, file=sys.stdout, desc="进度")
        update = lambda *args: pbar.update()
        proxymulti = multiprocessing.Process(target=proxy_add, args=(my_list, neek, appkey))
        proxymulti.start()
        for line in f:
            if tmp == "1":
                p.apply_async(getIpadcheck, args=(line.strip(), auth, "1", my_list, codeOk, codeErr), callback=update)
            elif tmp == "2":
                p.apply_async(getIpadcheck, args=(line.strip(), auth, "2", my_list, codeOk, codeErr), callback=update)

        p.close()
        p.join()

        pbar.write("-----------------------------不可用码----------------------------------")
        for a in codeErr: pbar.write(a)
        pbar.write("-----------------------------可用码----------------------------------")
        for a in codeOk: pbar.write(a)

        proxymulti.join()
    except Exception as e:
        print(e)
        input("程序出错·········")
