from urllib import request, parse
from bs4 import BeautifulSoup
import re
import os
from LinkChapters import getLinkChapters
from getLinkImage import getImage

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def folderName(url):
    directory = "C:/Users/ACer/Desktop"
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
    url = ["https://blogtruyen.com/6567/the-gamer-6567"]
    for link in url:
        downloadComic(link)

if __name__ == "__main__":
    main()
