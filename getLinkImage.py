from bs4 import BeautifulSoup
import requests
from headers import *

def get_image(url):
    req = requests.get(url, headers=headers)
    if req.status_code != 200:
        raise "get_image: request error"
    source = req.content
    soup = BeautifulSoup(source, 'html.parser')

    body = soup.body
    if "nettruyen" in url:
        link = body.find('div', class_ = 'reading-detail box_doc')
    elif "blogtruyen" in url:
        link = body.find('article', id = 'content')
    elif 'tctruyen' in url:
        link = body.find('div', id='contain-chapter')

    link_images = []
    for i in link.find_all('img'):
        src = i.get('src')
        if "https:" not in src:
            src = "https:" + src
        link_images.append(src)

    return link_images
