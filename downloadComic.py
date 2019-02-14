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

class downloadComic(threading.Thread):
    def __init__(self, url, lock):
        threading.Thread.__init__(self)
        self.url = url
        self.lock = lock

    def run(self):
        link_chapters = getLinkChapters(self.url)
        while link_chapters:
            try:
                link_chap = link_chapters.pop()
                link_images = getImage(link_chap)
                j = 1
                directory = "/Users/ACer/Desktop/" + "chap" + str(j)
                createFolder(directory)
                for i in range(len(link_images)):
                    image_name = directory + "/" + str(i) + ".jpg"
                    request.urlretrieve(link_images[i], image_name)
                j = j + 1
            except:
                pass
            self.lock.acquire()
            print("Download: ", link_chap, " done")
            self.lock.release()


def main():
    lock = threading.Lock()
    url1 = "https://blogtruyen.com/17777/van-co-kiem-than"
    url2 = "https://blogtruyen.com/20142/thien-tinh-chi-lo"
    # t1 = downloadComic(url1, lock)
    t2 = downloadComic(url2, lock)
    # t1.start()
    t2.start()
    # t1.join()
    t2.join()
    print("Done")

if __name__ == "__main__":
    main()