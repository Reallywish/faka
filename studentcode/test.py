# -*- coding:utf-8 -*-


from lxml import etree

if __name__ == '__main__':
    with open(".\\test.html", 'r', encoding='utf-8') as f:
        html = f.readline()

    html = etree.HTML(html, etree.HTMLParser(encoding="utf-8"))

    resright = html.xpath('//div[@class="col-right"]/text()')
    print("\t".join(resright))
