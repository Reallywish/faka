# -*- coding:utf-8 -*-

import urllib.parse

import requests

yourkey = '17602230628@b538688a53b806d45d284da6f7bca432'


def getUrl(url):
    encoded_url = urllib.parse.quote(url)
    request_url = f'http://api.985.so/api.php?url={encoded_url}&apikey={yourkey}'

    response = requests.get(request_url, verify=False).text
    return response


def main():
    with open("url", "r") as f:
        for line in f:
            print(line)


if __name__ == '__main__':
    print(getUrl(
        "https://email.myunidays.uk/system/clicked/1TEurs9PeEOPMyHsHIJrYXra02XGiIRJlvqG46j6zg0rdQ17Ugb0QKd1290iJSBMaHR0cHM6Ly93d3cubXl1bmlkYXlzLnVrL0NOL3poLUNOL3YvMjYwZDk1MzctMWJiYi00OTNjLWIwMzMtMTc4YWNmMmQ5NGJlP3JldHVyblVybD0lMmZDTiUyZnpoLUNOJTJmcGFydG5lcnMlMmZhcHBsZW11c2ljJTJmYWNjZXNzJTJmb25saW5lJnNvdXJjZT13d3cmc3R5bGU9ZGVmYXVsdCUyY2RlZmF1bHQlMmNmdWxsJnVpLXNpZz11NDZndW9JMVI4b0VXakU5bEhSM3B3JTNkJTNk"))
