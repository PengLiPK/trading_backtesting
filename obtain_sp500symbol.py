import datetime
import lxml.html
from urllib.request import urlopen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from db_declarative import Base, Daily_price, Data_vendor, Exchange, Symbol


def obtain_parse_wiki_snp500():
    """Download and parse the Wikipedia list of S&P500 
    constituents using requests and libxml.
    Returns a list of tuples for to add to SQL."""

    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use libxml to download the list of S&P500 companies and obtain the symbol table
    p = urlopen('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    page = lxml.html.parse(p)
    symbolslist = page.xpath('//table[1]/tr')[1:]

    # Obtain the symbol information
    symbols = []
    for symbol in symbolslist:
        tds = symbol.getchildren()
        try:
            sd = {'ticker': tds[0].getchildren()[0].text,
                  'name': tds[1].getchildren()[0].text,
                  'sector': tds[3].text}
            symbols.append((sd['ticker'],'stock',sd['name'],
                   sd['sector'],'USD',now,now))
        except Exception as e:
            pass
    return symbols


def insert_snp500_symbols(symbols):

    # Open data base
    engine = create_engine('sqlite:///exchage_sqlite3.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for a in symbols:
        newsymbol = Symbol(ticker=a[0],instrument=a[1],name=a[2],sector=a[3],
                      currency=a[4],created_date=a[5],last_updated_date=a[6])
        session.add(newsymbol)
    session.commit()

if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    print(len(symbols))
    print(symbols[0:3])
    insert_snp500_symbols(symbols)