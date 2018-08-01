from bs4 import BeautifulSoup

import requests

HOST = "http://www.btbtdy.net"


def processing_index():
    result = []
    r = requests.get('http://www.btbtdy.net/new/')
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    li_list = soup.find_all('li', class_="li")
    for li in li_list:
        div_list = li.find_all('div')
        if 'name' in div_list[0]['class']:
            data = {
                'href': "http://www.btbtdy.net/" + div_list[0].a['href'],
                'title': div_list[0].a.text,
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
    print(processing_index())
    # print(processing_detail('http://www.btbtdy.net//btdy/dy13279.html'))
