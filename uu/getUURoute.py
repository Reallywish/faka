# -*- coding:utf-8 -*-

import re
import os
import sys
import simplejson as json

try:
    interface = sys.argv[1]
except:
    interface = "172.19.83.237"


def __netmask_to_bit_length(netmask):
    count = sum([bin(int(i)).count('1') for i in netmask.split('.')])
    return int(count)


def get_sys_route():
    sys_route_table = os.popen('route print')  # 使用os.popen()获取程序输出
    all_route_lines = sys_route_table.readlines()  # 按行读取
    start_inx, end_inx = [inx for inx, line in enudmerate(all_route_lines) if line == '\n']  # 使用\n分割出路由表的起始行和结束行
    ipv4_route_lines = all_route_lines[start_inx + 5:end_inx - 1]  # 所有ipv4路由字符串列表

    f = open("./route.cmd", "w+")
    f1 = open("./route", "w+")
    a = []

    for line in ipv4_route_lines:
        # route, mask, gateway, interface, hops = re.findall(r'\S+', line)  # 网络路由地址,掩码,网关,跃点数
        if interface in line:
            # print(line)
            test = re.findall(r'\S+', line)
            # print(line)
            f.write("route add " + test[0] + " mask " + test[1] + " 192.168.123.1 if {} metric 5\n")
            count = __netmask_to_bit_length(test[1])
            ip = '{}/{}'.format(test[0], count)
            a.append(ip)
    f1.write(json.dumps(a))


if __name__ == '__main__':
    get_sys_route()
    # print(IP("184.87.133.2").make_net("255.255.255.255"))
