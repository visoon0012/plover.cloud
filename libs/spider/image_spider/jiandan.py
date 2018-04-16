import json

import requests
from bs4 import BeautifulSoup


def processing(soup):
    result = []
    a_list = soup.find_all('a')
    for a in a_list:
        if 'view_img_link' in str(a):
            result.append(a['href'])
    return result


if __name__ == '__main__':
    # response = requests.get("http://jandan.net/ooxx/page-1")
    # soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    # print(processing(soup))
    import requests

    url = "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2461815940.jpg"

    headers = {
        'cache-control': "no-cache",
        'postman-token': "47395395-8d24-7a21-a64d-e52f8e4ded35"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
