import pandas as pd
from sqlalchemy import create_engine


def db_sql(query: str, db):
    """

    :param query:
    :return:
    """
    try:
        return pd.read_sql(query, db)
    except Exception as e:
        print(e)


url = 'postgres://vkphdmoa:5f6f_ePBl4kYzF1ychIblsfbYESNaZ0X@dumbo.db.elephantsql.com:5432/vkphdmoa'

db = create_engine(url)


query = """SELECT title,author,published_date FROM articles.twentymin 
            order by published_date desc
            limit 10"""
df = db_sql(query, db)
print(df.head())


