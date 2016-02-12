import datetime
import lxml.html
from urllib.request import urlopen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from db_declarative import Base, Daily_price, Data_vendor, Exchange, Symbol


def obtain_list_of_db_tickers():
    """Obtains a list of the ticker symbols in the database."""

    # Open data base
    engine = create_engine('sqlite:///exchage_sqlite3.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    tickers = session.query(Symbol.id,Symbol.ticker).all()

    return tickers



def get_daily_historic_data_yahoo(ticker,
                                  start_date=(2000,1,1),
                                  end_date=datetime.date.today().timetuple()[0:3]):
    """Obtains data from Yahoo Finance returns and a list of tuples. """

    # Construct the Yahoo URL with the correct integer query parameters
    yahoo_url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % \
            (ticker,start_date[1] - 1,start_date[2],start_date[0],end_date[1] - 1,end_date[2],end_date[0])

    try:
        yh_data = urlopen(yahoo_url).readlines()[1:]
        prices = []

        for yh in yh_data:
            p = yh.strip().decode().split(',')
            prices.append( (datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                  p[1], p[2], p[3], p[4], p[5], p[6]) )
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)

    return prices


def insert_daily_price(data_vendor_id,symbol_id,daily_data):
    """Takes a list of tuples of daily data and adds it to the with vendor id and symbol id. """

    now = datetime.datetime.utcnow()

    # Open data base
    engine = create_engine('sqlite:///exchage_sqlite3.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for a in daily_data:
        new_dp = Daily_price(data_vendor_id=data_vendor_id,symbol_id=symbol_id,
            price_date=a[0],created_date=now,last_updated_date=now,open_price=a[1],
            high_price=a[2],low_price=a[3],close_price=a[4],volume=a[5],
            adj_close_price=a[6])
        session.add(new_dp)
    session.commit()


if __name__ == "__main__":
    tickers = obtain_list_of_db_tickers()
    for t in tickers:
        print("Adding data for %s" % t[1])
        yf_data = get_daily_historic_data_yahoo(t[1])
        insert_daily_price('1',t[0],yf_data)
