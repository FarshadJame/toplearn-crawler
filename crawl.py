import json
from abc import ABC, abstractmethod
import requests
from pars import BlogPageParser
from config import URL
from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data):
        pass

    @staticmethod
    def get(url, page_id=None):
        res = requests.get(url + str(page_id))

        if res.status_code == 200:
            return res

        return None


class LinkCrawler(BaseCrawler):
    def start(self, store=False):
        if store:
            self.store(self.start_crawl())

    def store(self, data):
        with open('archives/data.json', 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def find_links(html_doc):

        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.select('.article-col > .box-shadow > h2 > a')

    def start_crawl(self):
        page_id = 1
        crawl = True
        blog_list = list()
        while crawl:
            response = self.get(URL, page_id)
            links = self.find_links(response.text)
            if len(blog_list) > 1:
                if links[0].get('href') == blog_list[0].get('href'):
                    break
            page_id = page_id + 1
            blog_list.extend(links)
        print('find links successfully done!')
        return ['https://toplearn.com' + li.get('href') for li in blog_list]


class DataCrawler(BaseCrawler):
    def __init__(self):
        self.links = self.__load_links()
        self.parser = BlogPageParser()

    @staticmethod
    def __load_links():
        with open('archives/data.json', 'r') as f:
            return json.loads(f.read())

    def start(self, store=False):
        for link in self.links:
            response = self.get(link)
            data = self.parser.parse(response.text)
            if store:
                self.store(data)

    def store(self, data):
        filename = data['short_link'].split('/')[-1]
        with open(f'archives/blogs/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'archives/blogs/{filename}.json')
