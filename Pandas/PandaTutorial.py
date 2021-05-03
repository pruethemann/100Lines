import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os

def db_sql(query):
    return pd.read_sql(query, db)

#db = create_engine(os.environ['DB_URL']).connect()
db = create_engine("postgresql://postgres:kzu7@localhost/dvdrental")


df = db_sql("""
    SELECT 
        *
    FROM
        public.payment
    limit 100
""")

print(df.head(10))

df['index'] = df.index

id = df['rental_id']
update = df['payment_date']
amount = df['amount']

df.plot(x='index', y='amount')
plt.show()


