# -*- coding: utf-8 -*-
import netaddr


def merge():
    exclude = ['www.google.com', 'google.com', 'google.net', 'youtube.com',
               'www.youtube.com', 'youtube.net', 'twitter.com', 'twitter.net',
               'www.twitter.com', 'facebook.com', 'facebook.net', 'www.facebook.com',
               'akamaihd.net', 'akamaihd.net', 'www.akamaihd.net']
    exclude.sort()
    with open('./test.log', 'r') as f:
        lines = f.readlines()
        ips = []
        domains = []
        for i in lines:
            if ' -> ' in i:
                line = i.split(' -> ')[-1]
                if line[0].isdigit() and line.split(':')[0] not in ips and '.com' not in line.split(':')[0]:
                    if line.split(':')[0][-1].isdigit():
                        ips.append(line.split(':')[0])
                elif not (line[0].isdigit()) and line.split(':')[0] not in domains:
                    domains.append(line.split(':')[0])
                elif line[0].isdigit() and line.split(':')[0] not in ips and '.com' in line.split(':')[0]:
                    if '.'.join(line.split(':')[0].split('.')[-3::]) not in domains:
                        domains.append('.'.join(line.split(':')[0].split('.')[-3::]))
    ips.sort()
    domains.sort()
    domains2 = []
    for i in domains:
        if len(i.split('.')) >= 2 and '.'.join(i.split('.')[-2::]) not in domains2:
            domains2.append('.'.join(i.split('.')[-2::]))
    res = netaddr.cidr_merge(ips)
    for i in range(len(res)):
        res[i] = '.'.join(str(res[i]).split('.')[-4:-1]) + '.0/24'
    domains = domains + domains2
    for i in exclude:
        if i in domains:
            domains.remove(i)
    if '8.8.8.0/24' in res:
        res.remove('8.8.8.0/24')
    print(','.join(res))
    print()
    print(','.join(domains))


if __name__ == '__main__':
    merge()
