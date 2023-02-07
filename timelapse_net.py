#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import ConfigParser
import requests
import time
import sys
import re
from subprocess import Popen,PIPE

PINGFILE = './net_ping_delay.conf.default'
pingconfig = ConfigParser.RawConfigParser()
pingconfig.read(PINGFILE)

def poster(url,p,headers={}):
    try:
        r = requests.post(url, data=json.dumps(p), timeout=30,headers=headers)
        return r.text
    except:
        return None


FALCON_URL = 'http://127.0.0.1:1988/v1/push'

def corePing(endpoint='',username='root',port=22):
    """
    触发fping
    :param username:
    :param endpoint: endpoint
    :param port:
    :return:
    """
    try:
        dv_ips = pingconfig.options("ip2short")
        if endpoint == '':
           endpoint = pingconfig.get("endpoint","name")

        print("fping  -p 500 -q -c 60 -i 1 {ips}".format(ips = " ".join(dv_ips)))
        p = Popen("fping  -p 500 -q -c 60 -i 1 {ips}".format(ips = " ".join(dv_ips)),shell=True ,close_fds=True,stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()
        print(stderrdata)
        Townsend = []
        for presult in stderrdata.split('\n'):
            if presult != '' and re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).*",presult):
                presult_split = presult.split(':')
                if len(presult_split[1].split(',')) == 2:
                    loss = int(presult_split[1].split(',')[0].split('/').pop().rstrip('%'))
                    avg_rtt = presult_split[1].split(',')[1].split('/')[-2]
                else:
                    loss = 101
                    avg_rtt = 0

                Townsend.append({"metric": "ping.loss",
                                 "endpoint": endpoint,
                                 "timestamp": int(time.time()),
                                 "step": 60,
                                 "value": loss,
                                 "counterType": "GAUGE",
                                 "tags": "from={},to={}".format(endpoint,pingconfig.get("ip2short",presult_split[0].strip()))
                                 })

                Townsend.append({"metric": "ping.avg_rtt",
                                 "endpoint": endpoint,
                                 "timestamp": int(time.time()),
                                 "step": 60,
                                 "value": avg_rtt,
                                 "counterType": "GAUGE",
                                 "tags": "from={},to={}".format(endpoint,pingconfig.get("ip2short",presult_split[0].strip()))
                                 })
        print(poster(FALCON_URL, Townsend))
    except:
        print(sys.exc_info())

if __name__ == '__main__':
    corePing()
