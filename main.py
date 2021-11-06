import sys

from crawl import LinkCrawler

if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_links':
        crawler = LinkCrawler()
        crawler.start()
    elif switch == 'extract_pages':
        pass
