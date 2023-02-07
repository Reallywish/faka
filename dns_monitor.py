# -*- coding:utf-8 -*-
import time

import dns.resolver
import logging.handlers

import requests
import simplejson as json

LOG_FILENAME = './dns.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
format = "%(asctime)s %(process)d %(filename)s %(lineno)d %(levelname)s %(message)s"
handler = logging.handlers.WatchedFileHandler(LOG_FILENAME)
handler.setFormatter(logging.Formatter(format))
handler.suffix = "%Y%m%d"
logger.addHandler(handler)




def toOpenfalconCPE(value):
    url = "http://127.0.0.1:1988/v1/push"
    da = [{
        "Endpoint": "gamednsmonitor",
        "Metric": "dnsmonitor",
        "Timestamp": int(time.time()),
        "Step": 60,
        "Value": value,
        "CounterType": "GAUGE",
        "TAGS": ""
    }]
    try:
        response = requests.post(url, data=json.dumps(da)).text
        logger.info("push openfalcon res =====> " + str(response))
    except:
        logger.error("push openfalcon ERROR!!!")


if __name__ == '__main__':
    logger.info("-" * 50)
    myResolver = dns.resolver.Resolver()
    myResolver.nameservers = ['16.162.14.185']
    try:
        myAnswers = myResolver.query("pubwxp.vivox.com", "A")[0]
        logger.info("dns query is:===> " + str(myAnswers))
        if str(myAnswers) == '74.201.106.170':
            toOpenfalconCPE("1")
        else:
            toOpenfalconCPE("0")
    except:
        logger.error("get DNS ERROR!!!!")
        toOpenfalconCPE("0")