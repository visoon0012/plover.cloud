from bs4 import BeautifulSoup
from lxml import etree

import requests

HOST = "http://www.btbtdy.com"


def processing_index():
    result = []
    r = requests.get(HOST)
    r.encoding = 'utf-8'
    selector = etree.HTML(r.text)
    li_list = selector.xpath('//li[@class="li"]')
    for li in li_list:
        div_list = li.xpath('div')
        if 'name' in div_list[0].xpath('@class'):
            data = {
                'href': "http://www.btbtdy.net/" + div_list[0].xpath('a/@href')[0],
                'title': div_list[0].xpath('a/@title')[0],
                'source_type': div_list[4].text,
            }
            result.append(data)
    return result


def processing_detail(url):
    number = (url.split('/')[5]).replace('dy', '')
    url = 'http://www.btbtdy.net/vidlist/' + number + '?timestamp=0'
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    result = []
    for li in soup.find_all('li'):
        if "magnet:?xt=urn:btih:" in str(li):
            title = str(li.a['title'])
            data = {
                'download_link': li.a.next_sibling.a['href'],
                'name': title,
                'source': HOST
            }
            result.append(data)
    return result


if __name__ == '__main__':
    print(processing_detail('http://www.btbtdy.net//btdy/dy13279.html'))
