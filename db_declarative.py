from sqlalchemy import Column, ForeignKey, Integer, String, Time, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 

engine = create_engine('sqlite:///exchage_sqlite3.db') 
Base = declarative_base()
 
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    abbrev = Column(String(32), nullable=False)
    name = Column(String(255), nullable=False)
    city = Column(String(255))
    country = Column(String(255))
    currency = Column(String(64))
    timezone_offset = Column(Time)
    created_date = Column(DateTime, nullable=False)
    last_updated_date = Column(DateTime, nullable=False)
 
class Data_vendor(Base):
    __tablename__ = 'data_vendor'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    website_url = Column(String(255))
    support_email = Column(String(255))
    created_date = Column(DateTime, nullable=False)
    last_updated_date = Column(DateTime, nullable=False)

class Symbol(Base):
    __tablename__ = 'symbol'
    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer)
    ticker = Column(String(32), nullable=False)
    instrument = Column(String(64), nullable=False)
    name = Column(String(255))
    sector = Column(String(255))
    currency = Column(String(32))
    timezone_offset = Column(Time)
    created_date = Column(DateTime, nullable=False)
    last_updated_date = Column(DateTime, nullable=False)
    index_exchange_id = Column(Integer, ForeignKey('exchange.id'))
    exchange = relationship(Exchange)
 
class Daily_price(Base):
    __tablename__ = 'daily_price'
    id = Column(Integer, primary_key=True)
    data_vendor_id = Column(Integer, nullable=False)
    symbol_id = Column(Integer, nullable=False)
    price_date = Column(DateTime, nullable=False)
    created_date = Column(DateTime, nullable=False)
    last_updated_date = Column(DateTime, nullable=False)
    open_price = Column(Numeric(precision=19, scale=4))
    high_price = Column(Numeric(precision=19, scale=4))
    low_price = Column(Numeric(precision=19, scale=4))
    close_price = Column(Numeric(precision=19, scale=4))
    adj_close_price = Column(Numeric(precision=19, scale=4))
    volume = Column(Integer)
    index_data_vendor_id = Column(Integer, ForeignKey('data_vendor.id'))
    data_vendor = relationship(Data_vendor)
    index_symbol_id = Column(Integer, ForeignKey('symbol.id'))
    symbol = relationship(Symbol) 

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)