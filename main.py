import flask
from flask import request  # 获取参数
import simplejson as json
import requests
import hashlib

server = flask.Flask(__name__)

api_key = "50a768e3aade30ad281750cc30879d66"


def get_sign(data_str):
    """
    使用md5加密，返回sign
    :param data_str:
    :return:
    """
    m = hashlib.md5()
    m.update((api_key + data_str + api_key).encode('utf-8'))
    return m.hexdigest().casefold()


def get_comm_list():
    '''
    获取商品列表
    :return:
    '''
    url = "http://gameuu.sp.shay360.com/outerapi/api/router"

    payload = {'method': 'module.outerApi.getGoodsList',
               'user_name': '18234492659',
               'sign': '91a3f9e0f76bd500826a665d28ff6cde'}
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def create_order(goods_id, goods_number, outer_order_sn):
    """
    下单接口
    :param goods_id: 发卡网商品的id  200是天卡，201是三天卡，202是周卡，203是月卡，204是季卡，205是年卡
    :param goods_number: 要购买的数量
    :param outer_order_sn: 外部订单号
    :return:
    """

    prohibited_card_secret = open("./cards", "wb+")

    uri = "http://gameuu.sp.shay360.com/outerapi/api/router?"
    param = "goods_id={}&goods_number={}&method=module.outerApi.createUserOrder&outer_order_sn={}&user_name=18234492659".format(
        goods_id, goods_number, outer_order_sn)

    sign = get_sign(param)

    url = uri + param + "&sign=" + sign
    print(url)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, timeout=5).text
    # response = '{"code":0,"msg":"ok","data":{"card_list":["01TJ3UEYRJ3RB7ZKGX0P6PQ7YH7A"],"order_sn":"API_202203131138060389983","outer_order_sn":"888555222"}}'

    print(response)

    cards = json.loads(response)['data']['card_list']

    rescard = []

    tmp = 0

    for card in cards:
        print(card)
        if "QQ" in card or "WX" in card or "VX" in card:
            tmp += 1
            prohibited_card_secret.write(card + "\r\n")
        else:
            rescard.append(card)
    backupnum = len(cards) - tmp
    if backupnum < len(cards):
        result = create_order(goods_id, backupnum, outer_order_sn)
        return rescard + result
    else:
        return rescard


@server.route('/', methods=["post"])
def login():
    goods_id = request.values.get('goods_id')  # 获取参数
    goods_number = request.values.get('goods_number')
    outer_order_sn = request.values.get('outer_order_sn')

    responses = {}
    r = create_order(goods_id, goods_number, outer_order_sn)
    responses["code"] = 0
    responses["cards"] = r

    return responses


if __name__ == '__main__':
    server.run(port=8000, debug=True)  # debug设置为True，修改接口信息后直接刷新接口即可；添加参数host='0.0.0.0'允许同一局域网内访问
    # get_comm_list()
    # print(create_order(200, 1, "888555222"))
