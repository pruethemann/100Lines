import requests
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.sql import text
from datetime import datetime
from time import mktime
import feedparser
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging
import sys

class RSS:
    article_count = 0

    def __init__(self):
        logging.basicConfig(filename='blick.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

        #self.db = create_engine('postgresql://postgres:kzu7@localhost/Blick')
        self.db = create_engine('postgres://vkphdmoa:5f6f_ePBl4kYzF1ychIblsfbYESNaZ0X@dumbo.db.elephantsql.com:5432/vkphdmoa')


    def update_RSS(self):
        feeds_df = self.get_feed_urls()

        for feed_id in feeds_df.index:
            feed_url = feeds_df.loc[feed_id, 'url']
            feed = feedparser.parse(feed_url)

            for article in feed['items']:
                self.export(feed_id, article)

        logging.info(f'{self.article_count} articles imported')

    def db_sql(self, query:str):
        try:
            return pd.read_sql(query, self.db)
        except exc.OperationalError as e:
            print(e)
            logging.critical(e)
            sys.exit()

    def extractID(self, txt: str) -> int:
        code_str = txt[-14 : -5]
        code_str = re.sub("\D", "", code_str)
        return int(code_str)

    def extract_image_url(self, txt: str) -> str:
        if txt.__contains__('src="'):
            start = txt.find('src="') + 5
            end = txt.find('" />')
            return txt[start:end], txt[end+5:]
        return "", txt

    def extractAuthors(self, txt:str):
        txt = txt.replace(' und ', ',')
        return txt.split(',')

    def get_feed_urls(self):
        query = "SELECT * FROM articles.feed_blick"
        df = self.db_sql(query)
        df.index = df.id
        return df

    def check_id(self, id: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM articles.blick WHERE id = " + str(id) + ")"
        return self.db_sql(query).loc[0,'exists']

    def extract_metadata(self, a: feedparser.FeedParserDict):
        author = self.extractAuthors(a['author'])
        id = self.extractID(a['link'])
        image_url, summary = self.extract_image_url(a['summary'])
        date = datetime.fromtimestamp(mktime(a['published_parsed']))
        return a['title'], a['link'], author, summary, id, image_url, date

    def export(self, feed_id: int, article: feedparser.FeedParserDict) -> None:
        title, url, author, summary, id, image_url, date = self.extract_metadata(article)

        ## check if article already in db
        if self.check_id(id):
            self.update_type(id, feed_id)
            return

        ## Import full article
        soup = self.request_full_article(url)
        content = self.extract_content(soup)

        try:
            with self.db.connect() as con:
                data = ({"id": id, "title": title, "author": author, "published_date": date, "summary": summary, "content": content, "url": url, "image_url": image_url, "typ": [feed_id]},)
                statement = text("""INSERT INTO articles.blick(id, title, author, published_date, summary, content, url, image_url, type) VALUES(:id, :title, :author, :published_date, :summary, :content, :url, :image_url, :typ)""")
                for line in data:
                    con.execute(statement, **line)
                self.article_count += 1

        except Exception as e:
            logging.critical(f'Article {url} failed: {e}')

    def update_type(self,id:int, feed_id:int):
        query = f'SELECT type FROM articles.blick WHERE id = {id}'
        types = self.db_sql(query).loc[0,'type']
        if feed_id not in types:
            types.append(feed_id)
            txt = "'{"
            for t in types:
                txt += str(t) + ','
            txt = txt[:-1] + "}'"
            self.db.execute("""UPDATE articles.blick SET type = """ + txt +  """ WHERE id = """ + str(id ))

    def request_full_article(self, url: str) -> BeautifulSoup:
        try:
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'html.parser')
            return soup
        except Exception as e:
            print(e)

    def extract_content(self, soup: BeautifulSoup) -> str:
        content = str( soup.find_all(class_='article-body readmore') )
        #content = BeautifulSoup(content, features="lxml")
        #return content.get_text()[1:-1]
        return content[1:-1]


r = RSS()
r.update_RSS()

