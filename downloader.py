import os
from bs4 import BeautifulSoup
from headers import *
import requests
from threading import Thread

class Downloader:
    def __init__(self, url, directory="./"):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        url_split = self.url.split("/")
        self.directory = directory + url_split[-1]
        self.referer = url_split[2] + "/"
        self.workers = []

    def create_folder(self):
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
                self.absolute_path = os.path.abspath(self.directory)
        except OSError as err:
            raise Exception(
                'create directory {} failed: {}'.format(self.directory, err))

    def get_path(self):
        return self.absolute_path

    def done(self) -> bool:
        for w in self.workers:
            if w.is_alive():
                return False
        return True

    def download_worker(self, link_images, chap_idx):
        for i in range(len(link_images)):
            filename = "{}/chap{}-{}.jpg".format(self.directory, chap_idx, i)
            req = requests.get(link_images[i], headers=headers)
            if req.status_code != 200:
                raise Exception("get_image: request error with status code ",
                                req.status_code)
            try:
                with open(filename, 'wb') as file:
                    file.write(req.content)
            except Exception as err:
                raise Exception("write image error: ", err)

    def download_comic(self):
        self.get_link_chapters()
        self.create_folder()
        headers['referer'] = self.referer
        j = 1
        for i in range(len(self.link_chaps)):
            images = self.get_images_url(self.link_chaps[i])
            t = Thread(target=self.download_worker, args=(images,i+1))
            t.start()
            self.workers.append(t)

    def get_link_chapters(self):
        req = requests.get(self.url, headers=self.headers)
        if req.status_code != 200:
            raise Exception("get_link_chapters: request error with status code ",
                            req.status_code)

        source = req.content
        soup = BeautifulSoup(source, 'html.parser')
        body = soup.body
        self.link_chaps = []

        if "nettruyen" in self.url:
            link = body.find('div', class_='list-chapter')
            for i in link.find_all('a'):
                link = i.get('href')
                if '.' in link:
                    self.link_chaps.append(link)
        elif "blogtruyen" in self.url:
            link = body.find('div', id='list-chapters')
            for i in link.find_all('a'):
                link = i.get('href')
                self.link_chaps.append('https://blogtruyen.com/' + link)
        elif "tctruyen" in self.url:
            link = body.find('div', class_='comic-list-chapter')
            for i in link.find_all('a'):
                link = i.get('href')
                self.link_chaps.append(link)
        else:
            raise Exception("unexpected link")

    def get_images_url(self, chap_url):
        req = requests.get(chap_url, headers=headers)
        if req.status_code != 200:
            raise Exception("get_images_url: request error with status code ",
                            req.status_code)

        source = req.content
        soup = BeautifulSoup(source, 'html.parser')

        body = soup.body
        if "nettruyen" in chap_url:
            link = body.find('div', class_='reading-detail box_doc')
        elif "blogtruyen" in chap_url:
            link = body.find('article', id='content')
        elif 'tctruyen' in chap_url:
            link = body.find('div', id='contain-chapter')
        else:
            raise Exception("unexpected link")

        link_images = []
        for i in link.find_all('img'):
            src = i.get('src')
            if "https:" not in src:
                src = "https:" + src
            link_images.append(src)

        return link_images
