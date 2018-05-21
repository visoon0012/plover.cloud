import requests
from lxml import etree

HOST = "http://www.dy2018.com"


def processing_index():
    result = []
    r = requests.get(HOST)
    r.encoding = 'gb2312'
    selector = etree.HTML(r.text)
    a_list = selector.xpath('//li/a')
    for a in a_list:
        if '/i/' in str(etree.tostring(a)):
            data = {
                'href': HOST + a.xpath('@href')[0],
                'title': a.xpath('@title')[0]
            }
            result.append(data)
    return result


def processing_detail(url):
    result = []
    r = requests.get(url)
    r.encoding = 'gb2312'
    if r.text:
        selector = etree.HTML(r.text)
        title = selector.xpath('//div/div/h1')[0].text
        a_list = selector.xpath('//td/a')
        for a in a_list:
            if 'magnet' in str(etree.tostring(a)):
                data = {
                    'title': title,
                    'download_link': a.xpath('@href')[0],
                    'name': title,
                    'source': HOST
                }
                result.append(data)
            if '.mp4' in a.text or 'ftp' in a.text:
                data = {
                    'title': title,
                    'download_link': a.xpath('@href')[0],
                    'name': a.text,
                    'source': HOST
                }
                result.append(data)
    return result


if __name__ == '__main__':
    print(processing_detail('http://www.dy2018.com/i/98873.html'))
    pass
