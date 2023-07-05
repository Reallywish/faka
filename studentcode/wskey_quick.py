import multiprocessing
from multiprocessing import Pool, Manager

import base64  # 用于编解码
import json  # 用于Json解析
import os  # 用于导入系统变量
import sys  # 实现 sys.exit
import requests
import time  # 时间
import re  # 正则过滤
import hmac
import struct
import urllib3
import multiprocessing
from multiprocessing import Pool, Manager

urllib3.disable_warnings()


def ttotp(key):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', int(time.time() / 30))
    mac = hmac.new(key, counter, 'sha1').digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset + 4])[0] & 0x7fffffff
    return str(binary)[-6:].zfill(6)


def get_wskey():  # 方法 获取 wskey值 [系统变量传递]
    if "JD_WSCK" in os.environ:  # 判断 JD_WSCK是否存在于环境变量
        wskey_list = os.environ['JD_WSCK'].split('&')  # 读取系统变量 以 & 分割变量
        if len(wskey_list) > 0:  # 判断 WSKEY 数量 大于 0 个
            return wskey_list  # 返回 WSKEY [LIST]
        else:  # 判断分支
            print("JD_WSCK变量未启用")  # 标准日志输出
            sys.exit(1)  # 脚本退出
    else:  # 判断分支
        print("未添加JD_WSCK变量")  # 标准日志输出
        sys.exit(0)  # 脚本退出


# 返回值 list[jd_cookie]
def get_ck():  # 方法 获取 JD_COOKIE值 [系统变量传递] <! 此方法未使用 !>
    if "JD_COOKIE" in os.environ:  # 判断 JD_COOKIE是否存在于环境变量
        ck_list = os.environ['JD_COOKIE'].split('&')  # 读取系统变量 以 & 分割变量
        if len(ck_list) > 0:  # 判断 WSKEY 数量 大于 0 个
            return ck_list  # 返回 JD_COOKIE [LIST]
        else:  # 判断分支
            print("JD_COOKIE变量未启用")  # 标准日志输出
            sys.exit(1)  # 脚本退出
    else:  # 判断分支
        print("未添加JD_COOKIE变量")  # 标准日志输出
        sys.exit(0)  # 脚本退出


# 返回值 bool
# def check_ck(ck):  # 方法 检查 Cookie有效性 使用变量传递 单次调用
#     searchObj = re.search(r'pt_pin=([^;\s]+)', ck, re.M | re.I)  # 正则检索 pt_pin
#     if searchObj:  # 真值判断
#         pin = searchObj.group(1)  # 取值
#     else:  # 判断分支
#         pin = ck.split(";")[1]  # 取值 使用 ; 分割
#     if "WSKEY_UPDATE_HOUR" in os.environ:  # 判断 WSKEY_UPDATE_HOUR是否存在于环境变量
#         updateHour = 23  # 更新间隔23小时
#         if os.environ["WSKEY_UPDATE_HOUR"].isdigit():  # 检查是否为 DEC值
#             updateHour = int(os.environ["WSKEY_UPDATE_HOUR"])  # 使用 int化数字
#         nowTime = time.time()  # 获取时间戳 赋值
#         updatedAt = 0.0  # 赋值
#         searchObj = re.search(r'__time=([^;\s]+)', ck, re.M | re.I)  # 正则检索 [__time=]
#         if searchObj:  # 真值判断
#             updatedAt = float(searchObj.group(1))  # 取值 [float]类型
#         if nowTime - updatedAt >= (updateHour * 60 * 60) - (10 * 60):  # 判断时间操作
#             print(str(pin) + ";即将到期或已过期\n")  # 标准日志输出
#             return False  # 返回 Bool类型 False
#         else:  # 判断分支
#             remainingTime = (updateHour * 60 * 60) - (nowTime - updatedAt)  # 时间运算操作
#             hour = int(remainingTime / 60 / 60)  # 时间运算操作 [int]
#             minute = int((remainingTime % 3600) / 60)  # 时间运算操作 [int]
#             print(str(pin) + ";未到期，{0}时{1}分后更新\n".format(hour, minute))  # 标准日志输出
#             return True  # 返回 Bool类型 True
#     elif "WSKEY_DISCHECK" in os.environ:  # 判断分支 WSKEY_DISCHECK 是否存在于系统变量
#         print("不检查账号有效性\n--------------------\n")  # 标准日志输出
#         return False  # 返回 Bool类型 False
#     else:  # 判断分支
#         url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'  # 设置JD_API接口地址
#         headers = {
#             'Cookie': ck,
#             'Referer': 'https://home.m.jd.com/myJd/home.action',
#             'user-agent': ua
#         }  # 设置 HTTP头
#         try:  # 异常捕捉
#             res = requests.get(url=url, headers=headers, verify=False, timeout=10,
#                                allow_redirects=False)  # 进行 HTTP请求[GET] 超时 10秒
#         except Exception as err:  # 异常捕捉
#             print(str(err))  # 调试日志输出
#             print("JD接口错误 请重试或者更换IP")  # 标准日志输出
#             return False  # 返回 Bool类型 False
#         else:  # 判断分支
#             if res.status_code == 200:  # 判断 JD_API 接口是否为 200 [HTTP_OK]
#                 code = int(json.loads(res.text)['retcode'])  # 使用 Json模块对返回数据取值 int([retcode])
#                 if code == 0:  # 判断 code值
#                     print(str(pin) + ";状态正常\n")  # 标准日志输出
#                     return True  # 返回 Bool类型 True
#                 else:  # 判断分支
#                     print(str(pin) + ";状态失效\n")
#                     return False  # 返回 Bool类型 False
#             else:  # 判断分支
#                 print("JD接口错误码: " + str(res.status_code))  # 标注日志输出
#                 return False  # 返回 Bool类型 False


# 返回值 bool jd_ck
def getToken(args):  # 方法 获取 Wskey转换使用的 Token 由 JD_API 返回 这里传递 wskey
    wskey, index, result, url_t, ua, resulterr = args
    try:  # 异常捕捉
        url = str(base64.b64decode(url_t).decode()) + 'api/genToken'  # 设置云端服务器地址 路由为 genToken
        header = {"User-Agent": ua}  # 设置 HTTP头
        params = requests.get(url=url, headers=header, verify=False, timeout=20).json()  # 设置 HTTP请求参数 超时 20秒 Json解析
    except Exception as err:  # 异常捕捉
        print("Params参数获取失败")  # 标准日志输出
        print(str(err))  # 调试日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    headers = {
        'cookie': wskey,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': ua
    }  # 设置 HTTP头
    url = 'https://api.m.jd.com/client.action'  # 设置 URL地址
    data = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml%252fappjmp_blank.html%22%7D&'  # 设置 POST 载荷
    try:  # 异常捕捉
        res = requests.post(url=url, params=params, headers=headers, data=data, verify=False,
                            timeout=10)  # HTTP请求 [POST] 超时 10秒
        res_json = json.loads(res.text)  # Json模块 取值
        tokenKey = res_json['tokenKey']  # 取出TokenKey
    except Exception as err:  # 异常捕捉
        print("JD_WSKEY接口抛出错误 尝试重试 更换IP")  # 标准日志输出
        print(str(err))  # 标注日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    else:  # 判断分支
        return appjmp(wskey, tokenKey, ua, result, resulterr, index)  # 传递 wskey, Tokenkey 执行方法 [appjmp]


# 返回值 bool jd_ck
def appjmp(wskey, tokenKey, ua, result, resulterr, index):  # 方法 传递 wskey & tokenKey
    wskey = "pt_" + str(wskey.split(";")[0])  # 变量组合 使用 ; 分割变量 拼接 pt_
    if tokenKey == 'xxx':  # 判断 tokenKey返回值
        print(str(wskey) + ";疑似IP风控等问题 默认为失效\n--------------------\n")  # 标准日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    headers = {
        'User-Agent': ua,
        'accept': 'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-requested-with': 'com.jingdong.app.mall'
    }  # 设置 HTTP头
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
    }  # 设置 HTTP_URL 参数
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'  # 设置 URL地址
    try:  # 异常捕捉
        res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False,
                           timeout=20)  # HTTP请求 [GET] 阻止跳转 超时 20秒
    except Exception as err:  # 异常捕捉
        print("JD_appjmp 接口错误 请重试或者更换IP\n")  # 标准日志输出
        print(str(err))  # 标准日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    else:  # 判断分支
        try:  # 异常捕捉
            res_set = res.cookies.get_dict()  # 从res cookie取出
            pt_key = 'pt_key=' + res_set['pt_key']  # 取值 [pt_key]
            pt_pin = 'pt_pin=' + res_set['pt_pin']  # 取值 [pt_pin]
            if "WSKEY_UPDATE_HOUR" in os.environ:  # 判断是否在系统变量中启用 WSKEY_UPDATE_HOUR
                jd_ck = str(pt_key) + ';' + str(pt_pin) + ';__time=' + str(time.time()) + ';'  # 拼接变量
            else:  # 判断分支
                jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'  # 拼接变量
        except Exception as err:  # 异常捕捉
            print("JD_appjmp提取Cookie错误 请重试或者更换IP\n")  # 标准日志输出
            print(str(err))  # 标准日志输出
            return False, wskey  # 返回 -> False[Bool], Wskey
        else:  # 判断分支
            if 'fake' in pt_key:  # 判断 pt_key中 是否存在fake
                print(str(wskey) + ";WsKey状态失效\n")  # 标准日志输出
                resulterr.append(wskey)
                return False, wskey  # 返回 -> False[Bool], Wskey
            else:  # 判断分支
                print(str(wskey) + ";WsKey状态正常\n")  # 标准日志输出
                result[index] = jd_ck
                return True, jd_ck  # 返回 -> True[Bool], jd_ck


def cloud_info(url_t):  # 方法 云端信息
    url = str(base64.b64decode(url_t).decode()) + 'api/check_api'  # 设置 URL地址 路由 [check_api]
    for i in range(3):  # For循环 3次
        try:  # 异常捕捉
            headers = {"authorization": "Bearer Shizuku"}  # 设置 HTTP头
            res = requests.get(url=url, verify=False, headers=headers, timeout=20).text  # HTTP[GET] 请求 超时 20秒
        except requests.exceptions.ConnectTimeout:  # 异常捕捉
            print("\n获取云端参数超时, 正在重试!" + str(i))  # 标准日志输出
            time.sleep(1)  # 休眠 1秒
            continue  # 循环继续
        except requests.exceptions.ReadTimeout:  # 异常捕捉
            print("\n获取云端参数超时, 正在重试!" + str(i))  # 标准日志输出
            time.sleep(1)  # 休眠 1秒
            continue  # 循环继续
        except Exception as err:  # 异常捕捉
            print("\n未知错误云端, 退出脚本!")  # 标准日志输出
            print(str(err))  # 调试日志输出
            sys.exit(1)  # 脚本退出
        else:  # 分支判断
            try:  # 异常捕捉
                c_info = json.loads(res)  # json读取参数
            except Exception as err:  # 异常捕捉
                print("云端参数解析失败")  # 标准日志输出
                print(str(err))  # 调试日志输出
                sys.exit(1)  # 脚本退出
            else:  # 分支判断
                return c_info  # 返回 -> c_info


def check_cloud():  # 方法 云端地址检查
    url_list = ['aHR0cHM6Ly9hcGkubW9tb2UubWwv', 'aHR0cHM6Ly9hcGkubGltb2UuZXUub3JnLw==',
                'aHR0cHM6Ly9hcGkuaWxpeWEuY2Yv']  # URL list Encode
    for i in url_list:  # for循环 url_list
        url = str(base64.b64decode(i).decode())  # 设置 url地址 [str]
        try:  # 异常捕捉
            requests.get(url=url, verify=False, timeout=10)  # HTTP[GET]请求 超时 10秒
        except Exception as err:  # 异常捕捉
            print(str(err))  # 调试日志输出
            continue  # 循环继续
        else:  # 分支判断
            info = ['HTTPS', 'Eu_HTTPS', 'CloudFlare']  # 输出信息[List]
            print(str(info[url_list.index(i)]) + " Server Check OK\n--------------------\n")  # 标准日志输出
            return i  # 返回 ->i
    print("\n云端地址全部失效, 请检查网络!")  # 标准日志输出
    sys.exit(1)  # 脚本退出


def read_line(args):
    line, index, result = args
    # 在这里对读取的行进行处理，例如：
    processed_line = line.strip()
    # 将处理后的结果存储在共享列表中
    result[index] = processed_line


def main():
    input_file = "./wskyes.ini"
    # output_file = "./output.txt"

    url_t = check_cloud()  # 调用方法 [check_cloud] 并赋值 [url_t]
    cloud_arg = cloud_info(url_t)  # 调用方法 [cloud_info] 并赋值 [cloud_arg]
    ua = cloud_arg['User-Agent']

    # 使用 Manager 创建一个可在多个进程间共享的列表
    with Manager() as manager:
        # 读取输入文件的所有行
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 创建一个与输入文件行数相同长度的共享列表
        result = manager.list([None] * len(lines))
        resulterr = manager.list()

        # 创建进程池
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            # 使用 map 函数分配任务给多个进程
            pool.map(getToken, [(lines[i].strip(), i, result, url_t, ua, resulterr) for i in range(len(lines))])

        # 将结果写入输出文件
        # with open(output_file, "w", encoding="utf-8") as file:
        #     for line in result:
        #         file.write(line + "\n")
        print("-------------------------------可用-------------------------------")
        for o in result:
            if o:
                print(o)
        print("------------------------------不可用-------------------------------")
        for e in resulterr:
            print(e)
    input("回车结束·····")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input("出错了。请解决错误···")
