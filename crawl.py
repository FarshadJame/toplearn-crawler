import json
from abc import ABC, abstractmethod
import requests
from config import URL
from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass


class LinkCrawler(BaseCrawler):
    def start(self):
        self.store(self.start_crawl())

    def store(self, data):
        with open('archives/data.json', 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def get_page(url, page_id):
        res = requests.get(url.format(str(page_id)))

        if res.status_code == 200:
            return res

        return None

    @staticmethod
    def find_links(html_doc):

        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.select('.article-col > .box-shadow > h2 > a')

    def start_crawl(self):
        page_id = 1
        crawl = True
        blog_list = list()
        while crawl:
            response = self.get_page(URL, page_id)
            links = self.find_links(response.text)
            if len(blog_list) > 1:
                if links[0].get('href') == blog_list[0].get('href'):
                    break
            page_id = page_id + 1
            blog_list.extend(links)
        print('find links successfully done!')
        return ['https://toplearn.com' + li.get('href') for li in blog_list]


class DataCrawler(BaseCrawler):
    def start(self):
        pass

    def store(self, data):
        pass
