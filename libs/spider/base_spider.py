import re
import urllib.request

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(get_soup("http://www.piaohua.com"))
