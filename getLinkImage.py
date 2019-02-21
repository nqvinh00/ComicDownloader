from urllib import request, parse
from bs4 import BeautifulSoup
import re

def getImage(url):
    values = {'s': 'basic', 'submit': 'search'}
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0'
    data = parse.urlencode(values)
    data = data.encode('utf-8')
    req = request.Request(url, data, headers=headers)
    source = request.urlopen(req).read()
    soup = BeautifulSoup(source, 'html5lib')

    body = soup.body
    link = body.find('article', id = 'content')
    link_image = []
    for i in link.find_all('img'):
        link_image.append(i.get('src'))

    return link_image
