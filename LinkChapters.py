from urllib import request, parse
from bs4 import BeautifulSoup
import re

def getLinkChapters(url):
    values = {'s': 'basic', 'submit': 'search'}
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0'
    data = parse.urlencode(values)
    data = data.encode('utf-8')
    req = request.Request(url, data, headers=headers)
    source = request.urlopen(req).read()
    soup = BeautifulSoup(source, 'html5lib')

    body = soup.body
    link = body.find('div', id='list-chapters')
    link_chaps = []

    for i in link.find_all('a'):
        link_chaps.append('https://blogtruyen.com/' + i.get('href'))

    return link_chaps

# url = "https://blogtruyen.com/17777/van-co-kiem-than"