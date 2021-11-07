from bs4 import BeautifulSoup

from khayyam import JalaliDate


class BlogPageParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.select_one('.right-side h1 a')
        if title_tag:
            return title_tag.text

    @property
    def short_link(self):
        short_link = self.soup.select_one('.link')
        if short_link:
            return short_link.text

    @property
    def body(self):
        body = self.soup.select_one('.blog-main-content article')
        if body:
            return body.text

    @property
    def author(self):
        author = self.soup.select_one('.blog-details > ul > li:nth-child(3) > a')
        if author:
            return author.text

    @property
    def view(self):
        view = self.soup.select_one('.blog-details > ul > li:nth-child(1) > span')
        if view:
            return view.text

    @property
    def created_at(self):
        created_at = self.soup.select_one('.blog-details > ul > li:nth-child(2) > span')
        date = created_at.text.split('/')
        gregorian_date = JalaliDate(date[0], date[1], date[2]).todate()
        if gregorian_date:
            return str(gregorian_date.year) + '-' + str(gregorian_date.month) + '-' + str(
                gregorian_date.day)

    def parse(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=None, short_link=None, body=None, author=None, view=None, created_at=None
        )
        data['title'] = self.title
        data['short_link'] = self.short_link
        data['body'] = self.body
        data['author'] = self.author
        data['view'] = self.view
        data['created_at'] = self.created_at
        return data
