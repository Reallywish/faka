#! coding:utf-8

# from selenium import webdriver
#
#
#
# options = webdriver.FirefoxOptions()
# options.add_argument()
#
# browser = webdriver.Firefox('C:\\Users\\15986\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\9l4l8a5s.default-release')
# browser.set_preference("dom.webdriver.enabled", False)
# browser.get('http://www.baidu.com/')
import bs4
import requests
import simplejson as json

email = "CrqeNIBJ@snapmail.cc"

req = requests.get('https://snapmail.cc/emaillist/' + email)
if req.status_code == 200:
    # Get email text of the first email,
    # take "This is a test email." for example,
    # email_text = "This is a test email."
    for i in range(50000):
        # Get emails from an email box
        req = requests.get('https://snapmail.cc/emaillist/' + email)
        if req.status_code == 200:
            # Get email text of the first email,
            # take "This is a test email." for example,
            # email_text = "This is a test email."
            email_text = json.loads(req.text)[0]['html']
            try:
                soup = bs4.BeautifulSoup(email_text, 'lxml').find()
                print(soup)
                validation_code = str(soup).split("：")[1]
                print(validation_code)
                break
            except:
                print("解析邮件出错，可能不是Garena的邮件，返回内容如下：------------------------")
                print(email_text)

        print("获取邮箱验证码中。。。")
