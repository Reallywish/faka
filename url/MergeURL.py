# -*- coding: utf-8 -*-

import os
import configparser


def merge_log(filename, exclude):
    domains1 = []
    domains2 = []
    ips = []
    with open('./{}.txt'.format(filename), 'r') as f:
        txt = f.readlines()
    for i in range(len(txt)):
        txt[i] = txt[i].split('/')[2]
    txt = list(set(txt))
    for i in txt:
        if i[-1].isdigit():
            ips.append(i)
        elif len(i.split('.')) > 2:
            domains2.append('.'.join(i.split('.')[-2::]))
            domains1.append(i)
        else:
            domains2.append(i)
    domains = domains1 + domains2
    domains = list(set(domains) - set(exclude))
    for i in domains:
        if i[0].isdigit():
            domains.remove(i)
    domains.sort()
    for i in domains:
        print(i)
    print()
    # if ips:
    #     for i in ips:
    #         print(i)
    #     with open('./ips_list.log', 'w') as f:
    #         f.writelines(domains)
    # print()
    print(','.join(domains))
    # with open('./domains_merge.log', 'w') as f:
    #     f.writelines(','.join(domains))


def main():
    config = configparser.RawConfigParser()
    config.read('./Url.conf')
    exclude1 = config.get('Blacklist', 'Overseas').split(',')
    exclude2 = config.get('Blacklist', 'China').split(',')
    FileList = os.listdir('./')
    for i in FileList:
        if '.txt' in i:
            merge_log(i.split('.txt')[0], exclude1 + exclude2)


if __name__ == '__main__':
    main()
