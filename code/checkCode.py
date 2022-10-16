import requests

"""
平板msn：MHQR3CH/A
平板good_ids: 756

电脑msn：MLY33CH/A
电脑good_ids:1028
"""


class check:
    def __init__(self, studentCode, good_id, mpn):
        self.studentCode = studentCode
        self.good_id = good_id
        self.mpn = mpn

    def getcheck(self):
        url = "https://aar-orderapi.tjtjshengtu.com/api/h5app/wxapp/order/xxwCheck"
        payload = {'company_id': '1',
                   'xxw_check_code': self.studentCode,
                   'distributor_id': '2638',
                   'origin_bn': self.mpn,
                   'item_num': '1',
                   'goods_id': self.good_id}
        headers = {
            'authorizer-appid': 'wxd2678c430bfd3abc',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwOTAvYXBpL2g1YXBwL3d4YXBwL2xvZ2luIiwiaWF0IjoxNjY1NDEyMzE0LCJleHAiOjE2NjU4NDQzMTQsIm5iZiI6MTY2NTQxMjMxNCwianRpIjoickw5bjU3OTdXSUlrU3JpMiIsInN1YiI6IjM5MDMxNDdfZXNwaWVyX29adEdONUNEQkZDRGpwT0FLakd6LWRiZzh3RGtfZXNwaWVyX0Rpc3RpLTFjMGU3OGFjN2YwNGU4YWI0ZDE2NjUwNDgwNjIzNzQ3IiwicHJ2IjoiOTE1ZWYzYjE0NTc5N2Q5NjM2ZTY2Nzg2NjA4OWM2YmIxZmUzMmUxYyIsImlkIjoiMzkwMzE0N19lc3BpZXJfb1p0R041Q0RCRkNEanBPQUtqR3otZGJnOHdEa19lc3BpZXJfRGlzdGktMWMwZTc4YWM3ZjA0ZThhYjRkMTY2NTA0ODA2MjM3NDciLCJ1c2VyX2lkIjoiMzkwMzE0NyIsImRpc2FibGVkIjpmYWxzZSwiY29tcGFueV9pZCI6IjEiLCJ3eGFwcF9hcHBpZCI6Ind4ZDI2NzhjNDMwYmZkM2FiYyIsIndvYV9hcHBpZCI6bnVsbCwidW5pb25pZCI6IkRpc3RpLTFjMGU3OGFjN2YwNGU4YWI0ZDE2NjUwNDgwNjIzNzQ3Iiwib3BlbmlkIjoib1p0R041Q0RCRkNEanBPQUtqR3otZGJnOHdEayIsIm5pY2tuYW1lIjoiIiwibW9iaWxlIjoiNjQ5NDc3MzAwOTUiLCJ1c2VybmFtZSI6IiIsInNleCI6MCwidXNlcl9jYXJkX2NvZGUiOiI1MzVEQUE4MTQwQjIiLCJtZW1iZXJfY2FyZF9jb2RlIjoiNTM1REFBODE0MEIyIiwib2ZmbGluZV9jYXJkX2NvZGUiOiIiLCJvcGVyYXRvcl90eXBlIjoidXNlciJ9.5tr71AoJp50noc0tEOOEeHvCMeIyi11KJqejOI8gdyI',
            'Host': 'aar-orderapi.tjtjshengtu.com',
            'Connection': 'keep-alive',
            'Cookie': 'acw_tc=276077a416637677214626396e092c36258c50bbd68440ec4fc7161e0c7fc9'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(self.studentCode + "   结果：" + str(response.json()))


if __name__ == '__main__':
    f = open("./code", "r")
    for l in f.readlines():
        code = l.replace("\n", "")
        # check(code, "756", "MHQR3CH/A").getcheck()
        check(code, "1028", "MLY33CH/A").getcheck()
