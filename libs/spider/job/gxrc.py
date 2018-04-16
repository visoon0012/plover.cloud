import requests
from lxml import etree

HOST = "http://s.gxrc.com/"


def processing_list(url):
    result = []
    r = requests.get(url)
    selector = etree.HTML(r.text)
    div_list = selector.xpath('//div[@class="rlOne"]')
    for div in div_list:
        data = {}
        # ul1
        ul1 = div.xpath('ul')[0]
        data['href'] = ul1.xpath('li[@class="w1"]/h3/a')[0].xpath('@href')[0]  # 链接
        data['job_name'] = ul1.xpath('li[@class="w1"]/h3/a')[0].text  # 工作名称
        data['company_name'] = ul1.xpath('li[@class="w2"]/a')[0].text  # 公司名称
        data['amount'] = ul1.xpath('li[@class="w3"]')[0].text  # 薪资
        data['place'] = ul1.xpath('li[@class="w4"]')[0].text  # 上班地点
        data['update'] = ul1.xpath('li[@class="w5"]')[0].text  # 最后更新
        # ul2
        ul2 = div.xpath('ul')[1]
        li_list = ul2.xpath('li')
        data['number'] = li_list[0].xpath('span')[0].text  # 人数
        data['education'] = li_list[1].xpath('span')[0].text  # 学历
        data['experience'] = li_list[2].xpath('span')[0].text  # 经验
        data['nature'] = li_list[3].xpath('span')[0].text  # 公司性质
        result.append(data)
    return result


if __name__ == '__main__':
    processing_list('http://s.gxrc.com/sJob?schType=1&district=2&posType=5480%2C5483%2C5481&page=1&pageSize=20&orderType=3&listValue=1')
