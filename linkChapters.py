from bs4 import BeautifulSoup
from headers import *
import requests

def get_link_chapters(url):
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        raise "get_link_chapters: request error"
    source = req.content
    soup = BeautifulSoup(source, 'html.parser')

    body = soup.body
    link_chaps = []

    if "nettruyen" in url:
        link = body.find('div', class_='list-chapter')
        for i in link.find_all('a'):
            link_chaps.append(i.get('href'))
    elif "blogtruyen" in url:
        link = body.find('div', id='list-chapters')
        for i in link.find_all('a'):
            link_chaps.append('https://blogtruyen.com/' + i.get('href'))

    return link_chaps
