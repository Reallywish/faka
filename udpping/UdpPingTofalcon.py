#!/usr/bin/env python

from __future__ import print_function
import json
import requests
import socket
import time
import string
import random
import signal
import sys
import logging

# if not os.path.exists('./var/log/UdpPing/'):
#     os.system('mkdir -p /var/log/UdpPing/')

INTERVAL = 1000  # unit ms
LEN = 64
IP = ""
PORT = 0

count = 0
count_of_received = 0
rtt_sum = 0.0
rtt_min = 99999999.0
rtt_max = 0.0


def signal_handler():
    # if count != 0 and count_of_received != 0:
    #     print('')
    #     print('--- ping statistics ---')
    if count != 0:
        # print('%d packets transmitted, %d received, %.2f%% packet loss' % (
        #     count, count_of_received, (count - count_of_received) * 100.0 / count))
        logging.warning('%d packets transmitted, %d received, %.2f%% packet loss' % (
            count, count_of_received, (count - count_of_received) * 100.0 / count))
        SendFalcon(value=float((count - count_of_received) * 100.0 / count), metric='UdpPingLoss')
    if count_of_received != 0:
        # print('rtt min/avg/max = %.2f/%.2f/%.2f ms' % (rtt_min, rtt_sum / count_of_received, rtt_max))
        logging.info('rtt min/avg/max = %.2f/%.2f/%.2f ms' % (rtt_min, rtt_sum / count_of_received, rtt_max))
        SendFalcon(value=float(rtt_min), metric='UdpPingMin')
        SendFalcon(value=float(rtt_sum / count_of_received), metric='UdpPingAvg')
        SendFalcon(value=float(rtt_max), metric='UdpPingMax')


def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for m in range(length))


if len(sys.argv) != 7 and len(sys.argv) != 8:
    print(""" usage:""")
    print("""   this_program <dest_ip> <dest_port>""")
    print("""   this_program <dest_ip> <dest_port> "<options>" """)

    print()
    print(""" options:""")
    print("""   LEN         the length of payload, unit:byte""")
    print("""   INTERVAL    the seconds waited between sending each packet, 
    as well as the timeout for reply packet, unit: ms""")

    print()
    print(" examples:")
    print("   ./udpping.py 44.55.66.77 4000")
    print('   ./udpping.py 44.55.66.77 4000 "LEN=400;INTERVAL=2000"')
    print("   ./udpping.py fe80::5400:ff:aabb:ccdd 4000")
    print()

    exit()

IP = sys.argv[1]
PORT = int(sys.argv[2])
SIP = sys.argv[3]
falcon_host = sys.argv[4]
endpoint = sys.argv[5]
Tag = 'Pop=%s' % sys.argv[6]
is_ipv6 = 0

if IP.find(":") != -1:
    is_ipv6 = 1

if len(sys.argv) == 8:
    exec(sys.argv[7])

logging.basicConfig(format='%(asctime)s[%(levelname)s] %(module)s %(funcName)s %(lineno)d: %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S] ', level=logging.INFO, filename='./UdpPing_{}.log'.format(sys.argv[6]))


def SendFalcon(value, metric):
    url = "http://{}:{}/v1/push".format(falcon_host, '1988')
    ts = int(time.time())
    Payload = [{"endpoint": "{}".format(endpoint), "metric": metric, "timestamp": ts, "step": 60, "value": value,
                "counterType": "GAUGE", "tags": Tag}]
    requests.post(url=url, data=json.dumps(Payload))


if LEN < 5:
    print("LEN must be >=5")
    exit()
if INTERVAL < 50:
    print("INTERVAL must be >=50")
    exit()

signal.signal(signal.SIGINT, signal_handler)

if not is_ipv6:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

sock.bind((SIP, 0))

# print("UDPping %s via port %d with %d bytes of payload" % (IP, PORT, LEN))
sys.stdout.flush()

while True:
    payload = random_string(LEN)
    sock.sendto(payload.encode(), (IP, PORT))
    time_of_send = time.time()
    deadline = time.time() + INTERVAL / 1000.0
    received = 0
    rtt = 0.0

    while True:
        timeout = deadline - time.time()
        if timeout < 0:
            break
        # print "timeout=",timeout
        sock.settimeout(timeout)
        try:
            recv_data, addr = sock.recvfrom(65536)
            if recv_data == payload.encode() and addr[0] == IP and addr[1] == PORT:
                rtt = ((time.time() - time_of_send) * 1000)
                # print("Reply from", IP, "seq=%d" % count, "time=%.2f" % (rtt), "ms")
                sys.stdout.flush()
                received = 1
                break
        except socket.timeout:
            break
        except:
            pass
    count += 1
    if received == 1:
        count_of_received += 1
        rtt_sum += rtt
        rtt_max = max(rtt_max, rtt)
        rtt_min = min(rtt_min, rtt)
    else:
        logging.error("Request timed out")
        SendFalcon(value=100, metric='UdpPingLoss')
        SendFalcon(value=-1, metric='UdpPingMin')
        SendFalcon(value=-1, metric='UdpPingAvg')
        SendFalcon(value=-1, metric='UdpPingMax')
        sys.stdout.flush()

    if count == 60:
        try:
            signal_handler()
        except Exception as e:
            logging.error(Exception)
        count = 0
        count_of_received = 0
        rtt_sum = 0.0
        rtt_min = 99999999.0
        rtt_max = 0.0

    time_remaining = deadline - time.time()
    if (time_remaining > 0):
        time.sleep(time_remaining)
