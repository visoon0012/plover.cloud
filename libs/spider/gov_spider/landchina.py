import requests
from bs4 import BeautifulSoup
import time
import random
import sys


def get_post_data(url, headers):
    # 访问一次网页,获取post需要的信息
    data = {
        'TAB_QuerySubmitSortData': '',
        'TAB_RowButtonActionControl': '',
    }

    try:
        req = requests.get(url, headers=headers)
    except Exception as e:
        print('get baseurl failed, try again!', e)
    try:
        soup = BeautifulSoup(req.text, "html.parser")
        TAB_QueryConditionItem = soup.find(
            'input', id="TAB_QueryConditionItem270").get('value')
        # print TAB_QueryConditionItem
        data['TAB_QueryConditionItem'] = TAB_QueryConditionItem
        TAB_QuerySortItemList = soup.find(
            'input', id="TAB_QuerySort0").get('value')
        # print TAB_QuerySortItemList
        data['TAB_QuerySortItemList'] = TAB_QuerySortItemList
        data['TAB_QuerySubmitOrderData'] = TAB_QuerySortItemList
        __EVENTVALIDATION = soup.find(
            'input', id='__EVENTVALIDATION').get('value')
        # print __EVENTVALIDATION
        data['__EVENTVALIDATION'] = __EVENTVALIDATION
        __VIEWSTATE = soup.find('input', id='__VIEWSTATE').get('value')
        # print __VIEWSTATE
        data['__VIEWSTATE'] = __VIEWSTATE
    except Exception as e:
        print('get post data failed, try again!', e)
    return data


def get_info(url, headers):
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    items = soup.find(
        'table', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1")

    # 所需信息组成字典
    info = {}

    # 行政区
    division = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl").get_text().encode('utf-8')
    info['XingZhengQu'] = division

    # 项目位置

    location = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl").get_text().encode('utf-8')
    info['XiangMuWeiZhi'] = location

    # 面积(公顷)
    square = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl").get_text().encode('utf-8')
    info['MianJi'] = square

    # 土地用途
    purpose = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl").get_text().encode('utf-8')
    info['TuDiYongTu'] = purpose

    # 供地方式
    source = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl").get_text().encode('utf-8')
    info['GongDiFangShi'] = source

    # 成交价格(万元)
    price = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl").get_text().encode('utf-8')
    info['ChengJiaoJiaGe'] = price
    # print info
    # 用唯一值的电子监管号当key, 所需信息当value的字典
    all_info = {}
    Key_ID = items.find(
        'span', id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl").get_text().encode('utf-8')
    all_info[Key_ID] = info
    return all_info


def get_pages(baseurl, headers, post_data, date):
    print('date', date)
    # 补全post data
    post_data['TAB_QuerySubmitConditionData'] = post_data['TAB_QueryConditionItem'] + ':' + date
    page = 1
    while True:
        print('     page {0}'.format(page))
        # 休息一下,防止被网页识别为爬虫机器人
        time.sleep(random.random() * 3)
        post_data['TAB_QuerySubmitPagerData'] = str(page)
        req = requests.post(baseurl, data=post_data, headers=headers)
        # print req
        soup = BeautifulSoup(req.text, "html.parser")
        items = soup.find('table', id="TAB_contentTable").find_all(
            'tr', onmouseover=True)
        # print items
        for item in items:
            print(item.find('td').get_text())
            link = item.find('a')
            if link:
                print(item.find('a').text)
                url = 'http://www.landchina.com/' + item.find('a').get('href')
                print(get_info(url, headers))
            else:
                print('no content, this ten days over')
                return
        break
        page += 1


if __name__ == "__main__":
    # time.time()
    baseurl = 'http://www.landchina.com/default.aspx?tabid=263'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
        'Host': 'www.landchina.com'
    }

    post_data = (get_post_data(baseurl, headers))
    date = '2015-11-21~2015-11-30'
    get_pages(baseurl, headers, post_data, date)
