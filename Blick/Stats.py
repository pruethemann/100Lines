import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np

class Stats:
    df = ""

    def __init__(self):
        self.db = create_engine('postgresql://postgres:kzu7@localhost/Blick')
        #self.db = create_engine('postgres://vkphdmoa:5f6f_ePBl4kYzF1ychIblsfbYESNaZ0X@dumbo.db.elephantsql.com:5432/vkphdmoa')

    def db_sql(self, query:str):
        return pd.read_sql(query, self.db)

    def import_data(self):
        query = "SELECT * FROM articles.blick"
        self.df = self.db_sql(query)
        #self.df.published_date = pd.datetime(self.df.published_date)

    def plot(self):
        df = self.df
        df.published_date.hist(bins=20)
        plt.show()

    def author_plot(self):
        pd.set_option('display.max_columns', 10)
        self.df['date'] = self.df.published_date.dt.date

        df = self.df
        df['author'] = df['author'].apply(lambda x: x[0])
        author_stats = self.df.groupby(['author'])['author'].count()

        print(author_stats)

        #plt.pie(author_stats, labels = author_stats.index)
        plt.bar(author_stats.index, author_stats)
        plt.xticks(rotation=45)
        plt.show()



s = Stats()

s.import_data()
#s.plot()
#s.author_stats()
s.author_plot()
