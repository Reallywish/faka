# coding:utf-8
import time
import json
import os
import random
import bs4

import requests

# 获取毫秒级时间戳
timestamp = int(round(time.time() * 1000))


def makeUsername():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    username = ''.join(random.sample(alphabet, 8))
    print("生成的用户名：" + username)
    isUse = checkUsername(username)
    if isUse:
        print("用户名确定：{}".format(username))
        return username
    else:
        makeUsername()


def checkUsername(username):
    """
    检测用户名是否正确，  帳號限制 6 - 15 個字元，只能使用 a-z, A-Z, 0-9, 下引號(_), 引號(-) 與點(.)，設置的帳號必須有英文及數字，且頭尾不可為符號。

    :param username:
    :return:
    """
    url = "https://sso.garena.com/api/register/check?username={}&format=json&id={}".format(username, timestamp)

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.1.1264125623.1662193793; datadome=chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S; _ga_1M7M9L6VPX=GS1.1.1662193793.1.1.1662193965.0.0.0',
        'Referer': 'https://sso.garena.com/universal/register?redirect_uri=https://sso.garena.com/universal/login?app_id=10100%26redirect_uri=https%253A%252F%252Faccount.garena.com%252F%253Flocale_name%253DTW%26locale=zh-TW&locale=zh-TW',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-datadome-clientid': 'chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S'
    }

    response = requests.request("GET", url, headers=headers, data=payload).text
    print("检查用户名是否注册接口返回内容======>" + response)

    if "error" in response:
        return False
    else:
        return True


def checkMail(email):
    url = "https://sso.garena.com/api/register/check?email={}&format=json&id={}".format(email, timestamp)

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.1.1264125623.1662193793; datadome=chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S; _ga_1M7M9L6VPX=GS1.1.1662193793.1.1.1662193965.0.0.0',
        'Referer': 'https://sso.garena.com/universal/register?redirect_uri=https://sso.garena.com/universal/login?app_id=10100%26redirect_uri=https%253A%252F%252Faccount.garena.com%252F%253Flocale_name%253DTW%26locale=zh-TW&locale=zh-TW',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-datadome-clientid': 'chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S'
    }

    response = requests.request("GET", url, headers=headers, data=payload).text
    print("检查邮箱是否注册接口返回内容======>" + response)
    if "error" in response:
        return False
    else:
        return True


def sendmail(mail):
    url = "https://sso.garena.com/api/send_register_code_email"
    payload = "email={}&locale=zh-TW&format=json&id={}".format(mail, timestamp)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': '_ga=GA1.1.1264125623.1662193793; datadome=chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S; _ga_1M7M9L6VPX=GS1.1.1662193793.1.1.1662193965.0.0.0',
        'Origin': 'https://sso.garena.com',
        'Referer': 'https://sso.garena.com/universal/register?redirect_uri=https://sso.garena.com/universal/login?app_id=10100%26redirect_uri=https%253A%252F%252Faccount.garena.com%252F%253Flocale_name%253DTW%26locale=zh-TW&locale=zh-TW',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-datadome-clientid': 'chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S'
    }

    response = requests.request("POST", url, headers=headers, data=payload).text

    print("邮件发送结果：======>" + response)
    if "error" in response:
        return False
    else:
        return True


def get_verification_code(email):
    # We want to get account validation code in email
    validation_code = None
    # We will retry the request every 6 seconds to get the email
    for i in range(50000):
        # Get emails from an email box
        req = requests.get('https://snapmail.cc/emaillist/' + email)
        if req.status_code == 200:
            # Get email text of the first email,
            # take "This is a test email." for example,
            # email_text = "This is a test email."
            print(req.text)
            email_text = json.loads(req.text)[0]['html']
            try:
                soup = bs4.BeautifulSoup(email_text, 'lxml').td.p.get_text()
                validation_code = str(soup).split("：")[1]
                print(soup)
                break
            except:
                print("解析邮件出错，可能不是Garena的邮件，返回内容如下：------------------------")
                print(email_text)

        print("获取邮箱验证码中。。。")
        time.sleep(6)
    if validation_code:
        return validation_code


def register(username, email, emailcode):
    url = "https://sso.garena.com/api/register"

    payload = "username={username}&email={email}&email_otp={emailcode}&password=56418304294a963972fcc5697733e802efc0f4b0ae391a8bcfba34da842c4a0f15720c9f3fd3c97cd9df15ea3bd380d4eda40de372867e97b09d36ab1553df4b31b85b4a94f284715d10a9576b9691cf63d9aff5f3724c3944c0262dfb4a9d7f7c9ac33c3736ea86dfc6fa72df298d75f2f3813c7ecadc4f7fb6fb6be8ad6d81&location=SG&mobile_no=&otp=&locale=zh-TW&redirect_uri=https%3A%2F%2Fsso.garena.com%2Funiversal%2Flogin%3Fapp_id%3D10100%26redirect_uri%3Dhttps%253A%252F%252Faccount.garena.com%252F%253Flocale_name%253DTW%26locale%3Dzh-TW&format=json&id={timestamp}".format(
        username=username, email=email, emailcode=emailcode, timestamp=timestamp)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': '_ga=GA1.1.1264125623.1662193793; datadome=chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S; _ga_1M7M9L6VPX=GS1.1.1662193793.1.1.1662193965.0.0.0',
        'Origin': 'https://sso.garena.com',
        'Referer': 'https://sso.garena.com/universal/register?redirect_uri=https://sso.garena.com/universal/login?app_id=10100%26redirect_uri=https%253A%252F%252Faccount.garena.com%252F%253Flocale_name%253DTW%26locale=zh-TW&locale=zh-TW',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-datadome-clientid': 'chIs6Zd-lwz0LiyQyLKFFaIcO83-Z7VhVPX3hTmlXXIDinS2hRkH01h~nFlIhPpImUM45sPAa8U~A~ufcqeVH5C-UW3Km0dfv6c.Q4MiaxZXEL.Osuv51CpWW5Wq58S'
    }

    response = requests.request("POST", url, headers=headers, data=payload).text
    print(response)
    if "error" in response:
        print("注册失败！！！")
    else:
        print("恭喜，注册成功！！！")
        with open("./account.txt", "ab+") as f:
            f.write("{}----Abc123..\r\n".format(username).encode("utf-8"))


def start():
    # 获取用户名
    username = makeUsername()
    # 生成随机邮箱
    mail = "{}@snapmail.cc".format(username)
    # 检查邮箱是否可以注册
    if checkMail(mail):
        # 发送邮件
        sendStatus = sendmail(mail)
        if sendStatus:
            # 检查邮件
            mailcode = get_verification_code(mail)
            print(mailcode)
            register(username, mail, mailcode)


if __name__ == '__main__':
    for i in range(1, 2):
        start()
    # get_verification_code("xqsfkolu@snapmail.cc")
