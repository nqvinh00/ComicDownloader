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
    headers['referer'] = referer
    j = 1
    while link_chapters:
        try:
            link_images = get_image(link_chapters.pop())
            name = "{}./chap-{}".format(directory, j)
            create_folder(name)
            for i in range(len(link_images)):
                filename = "{}/{}.jpg".format(name, i)
                req = requests.get(link_images[i], headers=headers)
                with open(filename, 'wb') as file:
                    file.write(req.content)
            j += 1
        except:
            print("error")
            return
    print("Download: ", url, " done")
