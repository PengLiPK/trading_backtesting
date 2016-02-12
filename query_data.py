import datetime
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from db_declarative import Base, Daily_price, Data_vendor, Exchange, Symbol
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


# Open data base
engine = create_engine('sqlite:///exchage_sqlite3.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

close_price = []
price_date =[]
daily_prices = session.query(Daily_price).join(Symbol).filter(Symbol.ticker=='GOOG').all()
for daily_price in daily_prices:
	close_price.append(daily_price.close_price)
	price_date.append(daily_price.price_date)
	print(daily_price.price_date,daily_price.close_price)

data = {'Close price': close_price,
		'Date': price_date}
#sql = """SELECT * FROM daily_price WHERE symbol_id = 1 LIMIT 5"""

#goog = pd.read_sql(sa.text(sql),engine)

#print(goog.tail())

#google = pd.DataFrame(np.array(close_price),index=np.array(price_date))
g = pd.DataFrame(data)
gg = g.set_index('Date').astype('float')
print(gg.tail())
gg.plot()
plt.show()