from urllib import request, parse
from bs4 import BeautifulSoup
import re
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

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

def folderName(url):
    directory = "/Users/ACer/Desktop"
    pos = 0
    count = 0
    for i in range(len(url)):
        if url[i] == "/":
            count += 1
        if count == 4:
            pos = i
            break
    for i in range(pos, len(url)):
        directory += url[i]
    return directory

def downloadComic(url):
    link_chapters = getLinkChapters(url)
    directory = folderName(url)
    j = 1
    while link_chapters:
        try:
            link_images = getImage(link_chapters.pop())
            name = directory + "/chap" + str(j)
            createFolder(name)
            for i in range(len(link_images)):
                filename = name + "/" + str(i) + ".jpg"
                request.urlretrieve(link_images[i], filename)
            j = j + 1
        except:
            print("error")
    print("Download: ", url, " done")

def main():
    n = int(input())
    url = []
    while len(url) < n:
        print("Link:")
        link = input()
        url.append(link)

    for link in url:
        downloadComic(link)

if __name__ == "__main__":
    main()