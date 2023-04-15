import time

import requests
import threading
import simplejson as json


class MyThread(threading.Thread):
    def __init__(self, data, proxy_url, thread_num, num_threads):
        super().__init__()
        self.data = data
        self.proxy_url = proxy_url
        self.thread_num = thread_num
        self.num_threads = num_threads
        # 初始化 代理以及auth相关参数
        self.auth = open("./auth.ini", "r", encoding='utf-8-sig').readline().strip()
        self.proxy = None
        self.session = requests.Session()
        self.session.trust_env = False

    def run(self):
        if self.proxy is None:
            self.proxy = self.changeProxies(self.proxy_url)

        self.getIpadcheck(self.data)

    def getIpadcheck(self, studentCode):
        url = "https://aar-orderapi.tjtjshengtu.com/hyv80api/h5app/wxapp/order/xxwCheck"

        payload = f'company_id=1&xxw_check_code={studentCode}&distributor_id=3539&edu_param=&items%5B0%5D%5Borigin_bn%5D=MK2K3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=582&items%5B0%5D%5Bitem_name%5D=iPad%EF%BC%88%E7%AC%AC%E4%B9%9D%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=582'

        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': self.auth,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html',
        }

        try:
            response = self.session.request("POST", url, headers=headers, proxies=self.proxy, data=payload,
                                            timeout=10).json()
            if "True" in str(response):
                print(f"Thread {threading.current_thread().name} check studentCode {studentCode} succeeded")
            else:
                print(f"Thread {threading.current_thread().name} check studentCode {studentCode} failed")
        except Exception as e:
            # 如果报错，说明代理可能不可用，则更换代理 重新发起请求
            print(
                f"Thread {threading.current_thread().name} got exception while checking studentCode {studentCode}: {str(e)}")
            self.proxy = self.changeProxies(self.proxy_url)
            self.getIpadcheck(studentCode)

    def changeProxies(self, proxy_url):
        """
        小象、品易获取代理IP
        :param proxy_url:
        :return:
        """
        try:
            ret = requests.get(proxy_url)
            print(f"Thread {threading.current_thread().name} got proxies from API: {ret.text}")
        except Exception as e:
            print(f"Thread {threading.current_thread().name} failed to get proxies from API: {str(e)}")
            while True:
                try:
                    ret = requests.get(proxy_url)
                    break
                except:
                    continue

        while (json.loads(ret.text)['code'] != 200 and json.loads(ret.text)['code'] != 0):
            time.sleep(1)
            return self.changeProxies(proxy_url)

        try:
            data = json.loads(ret.text)['data'][0]
            proxies = {"https": f"{data['ip']}:{data['port']}"}
        except:
            data = ret.text.split(":")
            print(data)
            proxies = {"http": f"{data[0]}:{data[1]}"}

        print(f"Thread {threading.current_thread().name} is using proxy {proxies}")

        return proxies


# 创建数据列表
data_list = [line.rstrip('\n') for line in open('./studentcode', 'r')]

# 设置线程数
num_threads = 6

# 创建线程列表
threads = []

# 创建并启动线程
for i in range(num_threads):
    for j in range(len(data_list)):
        time.sleep(2)
        if j % num_threads == i:
            proxy_url = "http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek=65794&type=2&sep=4&sb=&ip_si=1&mr=0"  # 设置获取代理的URL
            thread = MyThread(data_list[j], proxy_url, i + 1, num_threads)
            thread.name = f"Thread-{i + 1}"
            threads.append(thread)
            thread.start()

# 等待所有线程执行完成
for thread in threads:
    thread.join()
