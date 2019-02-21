import os
import threading
from threading import Lock
from urllib import request
from LinkChapters import getLinkChapters
from getLinkImage import getImage

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def createFolderName(url):
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
    def __init__(self, urls, lock):
        threading.Thread.__init__(self)
        self.urls = urls
        self.lock = lock

    def run(self):
        self.lock.acquire()
        while self.urls:
            url = self.urls.pop()
            directory = createFolderName(url)
            createFolder(directory)
            link_chapters = getLinkChapters(url)
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
            print("Donwload: ", url, " done")
        self.lock.release()

def main():
    lock = threading.Lock()
    url = ["https://blogtruyen.com/17777/van-co-kiem-than"]
    url_ = ["https://blogtruyen.com/20142/thien-tinh-chi-lo"]
    t1 = downloadComic(url ,lock)
    t2 = downloadComic(url_, lock)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()

