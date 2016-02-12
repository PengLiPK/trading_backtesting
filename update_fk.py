from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_declarative import Base,Symbol,Daily_price

engine = create_engine('sqlite:///exchage_sqlite3.db')

Session = sessionmaker(bind=engine)
session = Session()


#symbols = session.query(Symbol).filter(Symbol.id==1).all()
symbols = session.query(Symbol).all()


for i in range(1,len(symbols)+1):
    for d_price in session.query(Daily_price).filter(Daily_price.symbol_id==i).all():
        d_price.symbol = symbols[i-1]

    print("%s finished!" % i)

session.commit()