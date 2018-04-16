import re

import requests
from bs4 import BeautifulSoup


def processing(base_url, id):
    response = requests.get(base_url % id)
    soup = BeautifulSoup(response.text, "html.parser")
    data = {
        'title': '',
        'tags': [],
        'content': '',
        'dynasty': '',
        'author': '',
    }
    div_id = soup.find('div', id='contson%s' % id)
    # 内容
    for content in div_id.contents:
        data['content'] += str(content).replace('\n', '')
    # 标题
    data['title'] = div_id.parent.h1.string
    # 朝代/作者
    count = 0
    for a in div_id.parent.find_all('a'):
        count += 1
        if count == 1:
            data['dynasty'] = a.string
        elif count == 2:
            data['author'] = a.string
    if 'class="tag"' in str(div_id.parent.parent):
        for a in div_id.parent.parent.find('div', class_='tag').find_all('a'):
            data['tags'].append(a.string)
    return data


if __name__ == '__main__':
    # content = get_soup('http://so.gushiwen.org/type.aspx?p=1')
    data = processing('http://so.gushiwen.org/view_%s.aspx', 1)
    # print(div_id.parent.prettify())
    print(data)
