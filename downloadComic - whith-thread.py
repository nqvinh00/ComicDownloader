import os
import threading
from urllib import request
from LinkChapters import getLinkChapters
from getLinkImage import getImage

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def createComicFolder(url):
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

class downloadComic(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        link_chapters = getLinkChapters(self.url)
        directory = createComicFolder(self.url)
        createFolder(directory)
        j = 1
        while link_chapters:
            try:
                link_chap = link_chapters.pop()
                link_images = getImage(link_chap)
                name = directory + "/chap" + str(j)
                createFolder(name)
                for i in range(len(link_images)):
                    image_name = name + "/" + str(i) + ".jpg"
                    request.urlretrieve(link_images[i], image_name)
                j = j + 1
            except:
                pass
            print("Download: ", link_chap, " done")

def main():
    url1 = "https://blogtruyen.com/17777/van-co-kiem-than"
    url2 = "https://blogtruyen.com/20142/thien-tinh-chi-lo"
    t1 = downloadComic(url1)
    t2 = downloadComic(url2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done")

if __name__ == "__main__":
    main()