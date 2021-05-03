import logging
import re
import sys
from datetime import datetime
from time import mktime

import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.sql import text


class RSS:
    article_count = 0

    def __init__(self):
        logging.basicConfig(filename='20min.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        #self.db = create_engine('postgresql://postgres:kzu7@localhost/Blick')
        self.db = create_engine('postgres://vkphdmoa:5f6f_ePBl4kYzF1ychIblsfbYESNaZ0X@dumbo.db.elephantsql.com:5432/vkphdmoa')

        self.update_RSS()

    def update_RSS(self):
        """

        """
        feeds_df = self.get_feed_urls()  # all 20 min feeds
        self.ids = self.fetch_id_sql()

        for feed_id in feeds_df.index:
            feed_url = feeds_df.loc[feed_id, 'url']
            feed = feedparser.parse(feed_url)

            for article in feed['entries']:
                self.fetch_article(article, feed_id)

        logging.info(f'{self.article_count} articles imported')

    def db_sql(self, query: str):
        """

        :param query:
        :return:
        """
        try:
            return pd.read_sql(query, self.db)
        except exc.OperationalError as e:
            print(e)
            logging.critical(e)
            sys.exit()


    def extract_id(self, txt: str) -> int:
        code_str = txt[-14:]
        code_str = re.sub("\D", "", code_str)
        if code_str == '':
            return 0
        return int(code_str)

    @staticmethod
    def extract_image_url(self, txt: str) -> str:
        if txt.__contains__('src="'):
            start = txt.find('src="') + 5
            end = txt.find('" />')
            return txt[start:end], txt[end + 5:]
        return "", txt

    def extractAuthors(self, txt: str):
        txt = txt.replace(' und ', ',')
        return txt.split(',')

    def fetch_id_sql(self):
        query = "SELECT id FROM articles.twentymin"
        df = self.db_sql(query)
        id_series = df.id.tolist()
        return id_series

    def fetch_authors(self):
        query = "SELECT author FROM articles.twentymin"
        df = self.db_sql(query)
        id_series = df.author.tolist()
        return id_series


    def get_feed_urls(self):
        query = "SELECT * FROM articles.feed_20min"
        df = self.db_sql(query)
        df.index = df.id
        return df

    def extract_data_feed(self, a: feedparser.FeedParserDict):
        title = a['title']
        url = a['link']
        id = self.extract_id(url)
        image_url = a['links'][1]['href']
        summary = a['summary_detail']['value']
        date = datetime.fromtimestamp(mktime(a['published_parsed']))
        return title, url, summary, id, image_url, date

    def fetch_article(self, article: feedparser.FeedParserDict, feed_id: int) -> None:
        title, url, summary, id, image_url, date = self.extract_data_feed(article)

        if id < 1000000:
            return

        if id in self.ids:
            return

        # Import full article
        soup = self.request_full_article(url)

        if '403 - Forbidden' in str(soup):
            return

        author, content, tags, isCommentable = self.extract_data_soup(soup)
        html = str(soup)
        self.insert_sql(title, url, summary, id, image_url, date, author, content, tags, isCommentable, html, feed_id)
        self.ids.append(id)

    def insert_sql(self, title, url, summary, id, image_url, date, author, content, tags, isCommentable,  html, feed_id):
        import_date = datetime.now()
        try:
            with self.db.connect() as con:
                data = ({"id": id, "title": title, "author": author, "published_date": date, "summary": summary,
                         "content": content, "url": url, "image_url": image_url, "tags": tags,
                         "isCommentable": isCommentable, "html":html, "feed_id":feed_id, "import_date": import_date},)
                statement = text("""INSERT INTO articles.twentymin(id, title, author, published_date, summary, content, url, image_url, tags, isCommentable, html, feed_id, import_date) 
                VALUES(:id, :title, :author, :published_date, :summary, :content, :url, :image_url, :tags, :isCommentable, :html, :feed_id, :import_date)""")
                for line in data:
                    con.execute(statement, **line)
                self.article_count += 1

        except Exception as e:
            print(e)
            logging.critical(f'Article {url} failed: {e}')

    def request_full_article(self, url: str) -> BeautifulSoup:
        try:
            page = requests.get(url, timeout=30)
            soup = BeautifulSoup(page.content.decode('ISO-8859-1', 'ignore'), 'html.parser')
            return soup
        except Exception as e:
            logging.critical(e)
            print(e)

    def extract_tags(self, soup):
        txt = soup.find('script', language='javascript')

        words = txt.text.split(' ')

        tag_reached = False
        for w in words:
            if tag_reached:
                break
            if w == "tags:":
                tag_reached = True
        w = w.replace("'", '')
        return w[:-2].split(',')

    def extract_content(self, soup: BeautifulSoup) -> str:
        txt = str(soup)

        start_tag = '<div class="story_text">'
        end_tag = '<p class="autor">'

        start = txt.find(start_tag)
        end = txt.find(end_tag)

        content = txt[start:end]

        content = BeautifulSoup(str(content), features="lxml")  # remove all <>
        return content.getText()

    def extract_beautiful(self, soup, class_=None) -> str:

        txt = soup.find_all(class_=class_)  # extract identifier

        content = BeautifulSoup(str(txt), features="lxml")  # remove all <>
        return content.get_text()

    def extract_data_soup(self, soup: BeautifulSoup) -> str:
        """

        :param soup:
        :return:
        """
        author = self.extract_beautiful(soup, class_='autor')
        author = author.replace('(', '')
        author = author.replace(')', '')
        author = author.replace(']', '')
        author = author.replace('[', '')
        author = author.split('/')
        content = self.extract_content(soup)
        tags = self.extract_tags(soup)
        tag = '<div class="add_comment">'
        isCommentable = tag in str(soup)
        return author, content.strip(), tags, isCommentable

r = RSS()

