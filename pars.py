from bs4 import BeautifulSoup


class BlogPageParser:
    @staticmethod
    def parse(html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(
            title=None, short_link=None, body=None, author=None, view=None, created_at=None
        )
        data = dict(title=None)
        title_tag = soup.select_one('.right-side h1 a')
        if title_tag:
            data['title'] = title_tag.text
        short_link = soup.select_one('.link')
        if short_link:
            data['short_link'] = short_link.text
        body = soup.select_one('.blog-main-content article')
        if body:
            data['body'] = body.text
        author = soup.select_one('.blog-details > ul > li:nth-child(3) > a')
        if author:
            data['author'] = author.text
        view = soup.select_one('.blog-details > ul > li:nth-child(1) > span')
        if view:
            data['view'] = view.text
        created_at = soup.select_one('.blog-details > ul > li:nth-child(2) > span')
        if created_at:
            data['created_at'] = created_at.text

        return data
