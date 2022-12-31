import os
import requests
from linkChapters import get_link_chapters
from getLinkImage import get_image
from headers import *

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def download_comic(url):
    link_chapters = get_link_chapters(url)
    split = url.split("/")
    directory, referer = split[-1], split[2] + "/"
    link_chapters = link_chapters[0:len(link_chapters) - 50]
    headers['referer'] = referer
    create_folder(directory)
    j = 1
    while link_chapters:
        l = link_chapters.pop()
        try:
            link_images = get_image(l)
            for i in range(len(link_images)):
                filename = "{}/chap{}-{}.jpg".format(directory, j, i)
                print(filename)
                req = requests.get(link_images[i], headers=headers)
                try:
                    with open(filename, 'wb') as file:
                        file.write(req.content)
                except Exception as e:
                    print(e)
                    return
            j += 1
        except:
            print("error: ", l)
            return
    print("Download: ", url, " done")
