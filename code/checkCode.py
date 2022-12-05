import requests

"""
平板msn：MHQR3CH/A
平板good_ids: 756

电脑msn：MLY33CH/A
电脑good_ids:1028
"""


class check:
    def __init__(self, studentCode):
        self.studentCode = studentCode

    def getMaccheck(self):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MLY33CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=1028&items%5B0%5D%5Bitem_name%5D=MacBook%20Air%20%28M2%29&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=1028".format(
            code=self.studentCode)
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM5MDMxNDdfZXNwaWVyX29adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGtfZXNwaWVyX29adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGsiLCJzdWIiOiIzOTAzMTQ3X2VzcGllcl9vWnRHTjVDREJGQ0RqcE9BS2pHei1kYmc4d0RrX2VzcGllcl9vWnRHTjVDREJGQ0RqcE9BS2pHei1kYmc4d0RrIiwidXNlcl9pZCI6MzkwMzE0NywiZGlzYWJsZWQiOjAsImNvbXBhbnlfaWQiOiIxIiwid3hhcHBfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ3b2FfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ1bmlvbmlkIjoib1p0R041Q0RCRkNEanBPQUtqR3otZGJnOHdEayIsIm9wZW5pZCI6Im9adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGsiLCJhdXRob3JpemVyX2FwcGlkIjoid3hkMjY3OGM0MzBiZmQzYWJjIiwib3BlcmF0b3JfdHlwZSI6InVzZXIifQ.47q4RWruuj3zYeuuearYDPvjRtpSox8r-Q7aqqkbUTI',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(self.studentCode + "   结果：" + str(response.json()))

    def getIpadcheck(self):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"

        payload = "company_id=1&xxw_check_code={code}&distributor_id=3655&edu_param=&items%5B0%5D%5Borigin_bn%5D=MM9F3CH%2FA&items%5B0%5D%5Bitem_num%5D=1&items%5B0%5D%5Bgoods_id%5D=899&items%5B0%5D%5Bitem_name%5D=iPad%20Air%EF%BC%88%E7%AC%AC%E4%BA%94%E4%BB%A3%EF%BC%89&items%5B0%5D%5Bis_edu%5D=1&items%5B0%5D%5Bitem_id%5D=899".format(
            code=self.studentCode)
        headers = {
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM5MDMxNDdfZXNwaWVyX29adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGtfZXNwaWVyX29adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGsiLCJzdWIiOiIzOTAzMTQ3X2VzcGllcl9vWnRHTjVDREJGQ0RqcE9BS2pHei1kYmc4d0RrX2VzcGllcl9vWnRHTjVDREJGQ0RqcE9BS2pHei1kYmc4d0RrIiwidXNlcl9pZCI6MzkwMzE0NywiZGlzYWJsZWQiOjAsImNvbXBhbnlfaWQiOiIxIiwid3hhcHBfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ3b2FfYXBwaWQiOiJ3eGQyNjc4YzQzMGJmZDNhYmMiLCJ1bmlvbmlkIjoib1p0R041Q0RCRkNEanBPQUtqR3otZGJnOHdEayIsIm9wZW5pZCI6Im9adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGsiLCJhdXRob3JpemVyX2FwcGlkIjoid3hkMjY3OGM0MzBiZmQzYWJjIiwib3BlcmF0b3JfdHlwZSI6InVzZXIifQ.47q4RWruuj3zYeuuearYDPvjRtpSox8r-Q7aqqkbUTI',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wxd2678c430bfd3abc/69/page-frame.html'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(self.studentCode + "   结果：" + str(response.json()))


if __name__ == '__main__':
    f = open("./code", "r")
    for l in f.readlines():
        code = l.replace("\n", "")
        check(code).getIpadcheck()
