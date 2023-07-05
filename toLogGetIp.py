# -*- coding: utf-8 -*-
import ipaddress
import os
import json
import time
import requests
from bs4 import BeautifulSoup


class GetCidrS:
    def __init__(self, debug=False):
        self.__url = "https://bgp.he.net/ip/"
        self.__CurlUrl = 'https://stat.ripe.net/data/routing-status/data.json?resource'
        self.__MessageUrl = 'https://api.ipregistry.co/%s?key=ssn0hc7wv1cfmhu4'
        self.__debug = debug

    def __get_message(self, IP_Num):
        url = self.__MessageUrl % IP_Num
        res = requests.request(method='get', url=url, timeout=10).text
        res = json.loads(res)
        if res["company"]["name"]:
            company = res["company"]["name"]
        else:
            company = 'Null'
        if res['connection']["asn"]:
            As = str(res['connection']["asn"])
        else:
            As = 'Null'
        if res["location"]['country']['name']:
            country = res["location"]['country']['name']
        else:
            country = 'Null'
        if res["location"]['city']:
            city = res["location"]['city']
        else:
            city = 'Null'
        return As, company, country, city

    def __GetHeader(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer': 'https://bgp.he.net/cc',
            'Cookie': '_gcl_au=1.1.1952279740.1683857510; __utmz=83743493.1683857511.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=83743493; c=BAgiFDE1Ni4yNTQuMTI1LjI1NA==--2a7e01d3c3b8332d154417a41a9dcad276b9662d; _bgp_session=BAh7BzoPc2Vzc2lvbl9pZEkiJTAyY2ViZWM1NWRhZTM4YmQ0MjdjZGEzZDM2ZGUxNjFjBjoGRUY6EF9jc3JmX3Rva2VuSSIxeDhUNW1sMUxIQ0RQY3pzNUdXeFpRUVBDWTNjTi9vYWpsYnlqSk1uMStYUT0GOwZG--9f28439701f177790794cbdf875f3e6d4a65b703; __utma=83743493.1201715895.1683857511.1684203110.1684208357.10; __utmt=1; __utmb=83743493.1.10.1684208357',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
            'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        if self.__debug:
            print(headers)
        return headers

    def __SendRes(self, IP_Num):
        url = self.__url + IP_Num
        headers = self.__GetHeader()
        response = requests.get(url=url, headers=headers)
        return response

    def __Merge_html(self, IP_Num, debug=False):
        response = self.__SendRes(IP_Num)
        # 解析HTML文档
        soup = BeautifulSoup(response.content, "html.parser")
        a, b = [], {}
        for i in soup.find('div', id='ipinfo').text.split('\n'):
            if i:
                a.append(i)
        lines = soup.find('div', id='whois').text.replace('        ', '').replace('  ', '').split('\n')
        for i in lines:
            if i:
                b.update({i.split(':')[0].strip(): i.split(':')[-1].strip()})
        a.pop(-1)
        if 'country' not in b:
            country = b['Country']
        else:
            country = b['country']
        if 'descr' not in b:
            org = b['OrgName']
        else:
            org = b['descr']
        if debug or self.__debug:
            print(a)
        ip = None
        for i in a:
            if '/' in i and i.split('/')[-1].isdigit():
                line = i
                if not ip:
                    ip = line
                else:
                    if int(line.split('/')[-1]) < int(i.split('/')[-1]):
                        ip = line
        return '{} {} {} {} {}'.format(ip, ' ' * 5, a[-1], country, org)

    def __GetCidrCurl(self, ip):
        command = '{}={}"'.format(self.__CurlUrl, ip)
        res = ''.join(os.popen(command).readlines())
        res = json.loads(res)
        res = '{} {}'.format(' '.join(self.__get_message(ip)), res['data']['first_seen']['prefix'])
        return res

    def __Judge(self, ip, cidrs):
        flag = False
        ip_obj = ipaddress.ip_address(ip)
        for cidr in cidrs:
            network = ipaddress.ip_network(cidr)
            if ip_obj in network:
                flag = True
        if self.__debug:
            print(flag)
        return flag

    def __GetRes(self, IP_Num, debug=False):
        res = self.__Merge_html(IP_Num, debug=debug)
        return IP_Num + ' ' * 5 + res

    def __StartModeOne(self, IP_Num):
        cidrs = []
        for i in IP_Num:
            try:
                if self.__Judge(i, cidrs):
                    continue
                else:
                    cidr = self.__GetCidrCurl(ip=i.split('/')[0])
                    cidrs.append(cidr)
                    time.sleep(1)
            except:
                cidr = '{}.0/24'.format('.'.join(i.split('.')[0:3]))
                cidrs.append(cidr)
                time.sleep(1)
        cidrs.sort()
        return cidrs

    def __StartModetwo(self, IP_Num):
        cidrs = []
        for i in IP_Num:
            try:
                if self.__Judge(i, cidrs):
                    continue
                else:
                    res = self.__GetRes(IP_Num=i.split('/')[0])
                    cidr = res.split(' ' * 5)[1].split(' ')[0]
                    cidrs.append(cidr)
                    time.sleep(1)
            except:
                cidr = '{}.0/24'.format('.'.join(i.split('.')[0:3]))
                cidrs.append(cidr)
                time.sleep(1)
        cidrs.sort()
        return cidrs

    def __MergeDomain(self, domains):
        if self.__debug:
            pass
        lines = []
        for i in domains:
            lines.append('.'.join(i.split('.')[-2::]))
        lines = list(set(lines))
        lines.sort()
        while not lines[0]:
            lines.pop(0)
        for j in ['com.hk', 'facebook.com', 'google.com']:
            if j in lines:
                lines.remove(j)
                for i in domains:
                    if j in i:
                        if 'www.{}'.format(j) in i:
                            continue
                        line = i.split('.{}'.format(j))[0]
                        if '.' in line:
                            line = '{}.{}'.format(line.split('.')[-1], j)
                        else:
                            line = '{}.{}'.format(line, j)
                        lines.append(line)
        lines = list(set(lines))
        lines.sort()
        return lines

    def Start(self, lines, Mode=1):
        lines = lines.split(',')
        ips, domains = [], []
        for i in range(len(lines)):
            if '(' in lines[i]:
                lines.append(lines[i].split('(')[-1])
        for i in range(len(lines)):
            lines[i] = lines[i].split(':')[0]
        lines = list(set(lines))
        lines.sort()
        for i in lines:
            if i[0].isdigit() and i[-1].isdigit():
                if i == '8.8.8.8':
                    continue
                ips.append(i)
            else:
                domains.append(i)
        if Mode == 1:
            ips = self.__StartModeOne(ips)
        elif Mode == 2:
            ips = self.__StartModetwo(ips)
        domains = self.__MergeDomain(domains)

        return ips, domains


def main():
    IP_Num = '103.254.155.196:443(vst.c.appier.net:443)",104.111.166.112:443(wv.inner-active.mobi:443)",104.116.243.16:443(p16-sign-sg.tiktokcdn.com:443)",104.116.243.27:443(p16-sign-sg.tiktokcdn.com:443)",104.116.243.32:443(tnc16-alisg.isnssdk.com:443)",104.116.243.8:443(pangolin16.sgsnssdk.com:443)",104.70.235.168:443(cdn2.inner-active.mobi:443)",104.70.235.186:443(cdn2.inner-active.mobi:443)",104.79.115.199:443(fgg9og-inapps.appsflyersdk.com:443)",104.79.115.199:443(fgg9og-launches.appsflyersdk.com:443)",121.4.9.179:443(adx-tk.rayjump.com:443)",13.214.254.38:443(sg01.rayjump.com:443)",13.224.167.107:443(se-new-cdn-ap-northeast-2a-hb.rayjump.com:443)",13.224.167.119:443(se-new-cdn-ap-northeast-2c-hb.rayjump.com:443)",13.224.167.19:443(outcome-ssp.supersonicads.com:443)",13.224.167.35:443(sg01-cdn.rayjump.com:443)",13.224.167.46:443(se-new-cdn-ap-northeast-2a-hb.rayjump.com:443)",13.224.167.5:443(se-new-cdn-ap-northeast-2a-hb.rayjump.com:443)",13.224.167.59:443(se-new-cdn-ap-northeast-2c-hb.rayjump.com:443)",13.224.167.61:443(se-new-cdn-ap-northeast-2c-hb.rayjump.com:443)",13.224.167.65:443(outcome-ssp.supersonicads.com:443)",13.224.167.73:443(impression.appsflyer.com:443)",13.224.167.7:443(se-new-cdn-ap-northeast-2a-hb.rayjump.com:443)",13.224.167.8:443(outcome-ssp.supersonicads.com:443)",13.225.103.105:443(cdn.liftoff-creatives.io:443)",13.225.103.107:443(newplayable.mintegral.com:443)",13.225.103.109:443(hybird.rayjump.com:443)",13.225.103.122:443(cdn.liftoff-creatives.io:443)",13.225.103.70:443(newplayable.mintegral.com:443)",13.226.120.114:443(rv-gateway.supersonicads.com:443)",13.226.120.117:443(assets.mintegral.com:443)",13.226.120.27:443(net-se-cdn.rayjump.com:443)",13.226.120.29:443(rv-gateway.supersonicads.com:443)",13.226.120.4:443(rv-gateway.supersonicads.com:443)",13.226.120.52:443(cdn-adn-https-new.rayjump.com:443)",13.226.120.61:443(is-gateway.supersonicads.com:443)",13.226.120.80:443(cdn-adn-https-new.rayjump.com:443)",13.226.120.82:443(impression.appsflyer.com:443)",13.226.120.88:443(is-gateway.supersonicads.com:443)",13.226.120.88:443(logs.ironsrc.mobi:443)",13.226.120.88:443(rv-gateway.supersonicads.com:443)",13.226.120.99:443(cdn-adn-https-new.rayjump.com:443)",13.227.53.105:443(networksdk.ssacdn.com:443)",13.228.63.134:443(sg01.rayjump.com:443)",13.228.63.134:443(tknet.rayjump.com:443)",13.250.130.0:443(sg01.rayjump.com:443)",13.251.0.5:443(sg01.rayjump.com:443)",13.251.0.5:443(tknet.rayjump.com:443)",142.250.182.131:443(142.250.182.131:443)",142.250.199.66:443(142.250.199.66:443)",142.250.199.66:443(pagead2.googleadservices.com:443)",142.250.204.130:443(142.250.204.130:443)",142.250.204.130:443(googleads.g.doubleclick.net:443)",142.250.204.66:443(pagead2.googlesyndication.com:443)",142.250.204.74:443(firebaseremoteconfig.googleapis.com:443)",142.250.207.65:443(142.250.207.65:443)",142.250.207.65:443(lh3.googleusercontent.com:443)",142.250.66.130:443(pagead2.googleadservices.com:443)",142.250.66.66:443(ade.googlesyndication.com:443)",142.250.66.66:443(googleads.g.doubleclick.net:443)",142.250.66.98:443(142.250.66.98:443)",142.250.66.98:443(pagead2.googlesyndication.com:443)",142.250.66.99:443(142.250.66.99:443)",142.250.66.99:443(www.gstatic.com:443)",142.250.75.227:443(142.250.75.227:443)",142.250.76.131:443(142.250.76.131:443)",142.251.130.2:443(googleads.g.doubleclick.net:443)",142.251.220.2:443(142.251.220.2:443)",142.251.220.2:443(googleads.g.doubleclick.net:443)",142.251.220.98:443(142.251.220.98:443)",142.251.220.98:443(pagead2.googlesyndication.com:443)",150.158.223.91:443(configv2.unityads.unitychina.cn:443)",157.240.199.17:443(graph.facebook.com:443)",172.217.24.226:443(172.217.24.226:443)",172.217.24.226:443(googleads.g.doubleclick.net:443)",172.217.24.226:443(static.googleadsserving.cn:443)",172.217.24.66:443(172.217.24.66:443)",172.217.24.66:443(googleads4.g.doubleclick.net:443)",172.217.24.66:443(googleads.g.doubleclick.net:443)",172.217.25.2:443(172.217.25.2:443)",172.217.25.3:443(fonts.gstatic.com:443)",172.217.27.2:443(googleads.g.doubleclick.net:443)",172.217.27.34:443(172.217.27.34:443)",172.217.27.38:443(172.217.27.38:443)",172.217.27.38:443(s0.2mdn.net:443)",172.217.31.2:443(googleads.g.doubleclick.net:443)",172.217.31.2:443(pagead2.googleadservices.com:443)",18.136.70.123:443(sg01.rayjump.com:443)",18.136.96.114:443(sg01.rayjump.com:443)",18.141.70.67:443(sg01.rayjump.com:443)",18.141.70.67:443(tknet.rayjump.com:443)",18.182.170.114:443(impression-asia.liftoff.io:443)",182.92.212.20:443(analytics.mintegral.net:443)",185.151.204.200:443(s2s.adjust.com:443)",185.151.204.50:443(view.adjust.com:443)",185.151.204.51:443(view.adjust.com:443)",216.239.32.3:443(csi.gstatic.com:443)",216.58.200.226:443(pagead2.googleadservices.com:443)",216.58.200.226:443(static.googleadsserving.cn:443)",23.211.136.35:443(p16-ttam-va.ibyteimg.com:443)",23.211.136.49:443(sf16-static.i18n-pglstatp.com:443)",23.211.136.75:443(p16-ttam-va.ibyteimg.com:443)",23.33.184.226:443(ad.appier.net:443)",23.33.184.229:443(ad.appier.net:443)",23.33.184.229:443(code.createjs.com:443)",23.33.184.234:443(ipp.appier.net:443)",23.33.184.235:443(ad.appier.net:443)",23.40.241.161:443(api16-log-sg2.pangle.io:443)",23.40.241.176:443(api16-access-sg.pangle.io:443)",23.40.241.176:443(api16-log-sg2.pangle.io:443)",23.40.241.184:443(mssdk-sg-bu.byteoversea.com:443)",23.40.241.194:443(api16-access-sg.pangle.io:443)",23.40.241.194:443(api16-log-sg2.pangle.io:443)",23.40.241.224:443(mssdk-sg-bu.byteoversea.com:443)",23.40.241.235:443(mssdk-sg-bu.byteoversea.com:443)",31.13.75.1:443(graph.facebook.com:443)",31.13.77.17:443(graph.facebook.com:443)",3.208.175.71:443(track.tenjin.io:443)",34.102.162.219:443(ms4.applovin.com:443)",34.102.162.219:443(ms.applovin.com:443)",34.102.162.219:443(prod-mediate-events.applovin.com:443)",34.102.178.164:443(auction-load.unityads.unity3d.com:443)",34.107.172.168:443(thind.unityads.unity3d.com:443)",34.110.167.12:443(auction-load.unityads.unity3d.com:443)",34.110.179.88:443(d.applovin.com:443)",34.117.123.243:443(events.mz.unity3d.com:443)",34.117.147.68:443(rt.applovin.com:443)",34.120.175.182:443(assets.applovin.com:443)",34.120.62.227:443(edge.safedk.com:443)",34.149.87.163:443(res1.applovin.com:443)",34.160.119.165:443(img.applovin.com:443)",34.160.254.144:443(pdn.applovin.com:443)",35.194.118.66:443(jprtb.c.appier.net:443)",35.227.198.107:443(sdk-diagnostics.prd.mz.internal.unity3d.com:443)",35.243.87.31:443(jprtb.c.appier.net:443)",39.107.225.241:443(net.rayjump.com:443)",44.196.50.154:443(us01.rayjump.com:443)",44.209.67.68:443(us01.rayjump.com:443)",45.43.60.2:443(api.metaverservers.com:443)",52.76.112.154:443(sg01.rayjump.com:443)",52.76.254.182:443(sg01.rayjump.com:443)",54.160.0.73:443(config.ads.vungle.com:443)",54.192.18.79:443(mtg-native.rayjump.com:443)",54.192.18.9:443(init.supersonicads.com:443)",54.205.243.176:443(us01.rayjump.com:443)",54.255.167.89:443(sg01.rayjump.com:443)",74.125.68.120:443(csi.gstatic.com:443)",8.8.8.8:53(8.8.8.8:53)",ad.appier.net:443",ade.googlesyndication.com:443",adx-tk.rayjump.com:443",analytics.mintegral.net:443",api16-access-sg.pangle.io:443",api16-log-sg2.pangle.io:443",api.metaverservers.com:443",assets.applovin.com:443",assets.mintegral.com:443",auction-load.unityads.unity3d.com:443",cdn2.inner-active.mobi:443",cdn-adn-https-new.rayjump.com:443",cdn.liftoff-creatives.io:443",code.createjs.com:443",config.ads.vungle.com:443",configv2.unityads.unitychina.cn:443",csi.gstatic.com:443",d.applovin.com:443",edge.safedk.com:443",events.mz.unity3d.com:443",fgg9og-inapps.appsflyersdk.com:443",fgg9og-launches.appsflyersdk.com:443",firebaseremoteconfig.googleapis.com:443",fonts.gstatic.com:443",googleads4.g.doubleclick.net:443",googleads.g.doubleclick.net:443",graph.facebook.com:443",hybird.rayjump.com:443",img.applovin.com:443",impression.appsflyer.com:443",impression-asia.liftoff.io:443",init.supersonicads.com:443",ipp.appier.net:443",is-gateway.supersonicads.com:443",jprtb.c.appier.net:443",lh3.googleusercontent.com:443",logs.ironsrc.mobi:443",ms4.applovin.com:443",ms.applovin.com:443",mssdk-sg-bu.byteoversea.com:443",mtg-native.rayjump.com:443",net.rayjump.com:443",net-se-cdn.rayjump.com:443",networksdk.ssacdn.com:443",newplayable.mintegral.com:443",outcome-ssp.supersonicads.com:443",p16-sign-sg.tiktokcdn.com:443",p16-ttam-va.ibyteimg.com:443",pagead2.googleadservices.com:443",pagead2.googlesyndication.com:443",pangolin16.sgsnssdk.com:443",pdn.applovin.com:443",prod-mediate-events.applovin.com:443",res1.applovin.com:443",rt.applovin.com:443",rv-gateway.supersonicads.com:443",s0.2mdn.net:443",s2s.adjust.com:443",sdk-diagnostics.prd.mz.internal.unity3d.com:443",se-new-cdn-ap-northeast-2a-hb.rayjump.com:443",se-new-cdn-ap-northeast-2c-hb.rayjump.com:443",sf16-static.i18n-pglstatp.com:443",sg01-cdn.rayjump.com:443",sg01.rayjump.com:443",static.googleadsserving.cn:443",thind.unityads.unity3d.com:443",tknet.rayjump.com:443",tnc16-alisg.isnssdk.com:443",track.tenjin.io:443",us01.rayjump.com:443",view.adjust.com:443",vst.c.appier.net:443",wv.inner-active.mobi:443",www.gstatic.com:443"'
    GCS = GetCidrS()
    ips, domains = GCS.Start(IP_Num, Mode=2)
    for i in ips:
        print(i)
    print()
    for i in domains:
        print(i)


if __name__ == '__main__':
    main()
