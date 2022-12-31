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
            link = i.get('href')
            if '.' in link:
                link_chaps.append(link)
    elif "blogtruyen" in url:
        link = body.find('div', id='list-chapters')
        for i in link.find_all('a'):
            link = i.get('href')
            link_chaps.append('https://blogtruyen.com/' + link)
    elif "tctruyen" in url:
        link = body.find('div', class_='comic-list-chapter')
        for i in link.find_all('a'):
            link = i.get('href')
            link_chaps.append(link)
    return link_chaps
