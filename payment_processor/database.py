from payment_processor.exceptions import *
import datetime

# Import sqlalchemy if not aviable the database module will be exlcuded
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Column, Integer, Float, String
    from sqlalchemy.ext.declarative import declarative_base
except ImportError:
    import logging
    logging.warning('SQLAlchemy not aviable, removing SQLCounter.')
    raise SQLEngineNotAviable('SQLAlchemy not aviable.')

TABLE_NAME = 'payment_processor'

Session = sessionmaker()

Base = declarative_base()

class CounterTable(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    provider = Column(String)
    day_amount_count = Column(Float)
    month_amount_count = Column(Float)
    day_trans_count = Column(Integer)
    month_trans_count = Column(Integer)
    day_count_timestamp = Column(String(8))
    month_count_timestamp = Column(String(6))

    def __init__(self, provider):
        self.provider = provider
        self.day_amount_count = 0.0
        self.month_amount_count = 0.0
        self.day_trans_count = 0
        self.month_trans_count = 0
        self.day_count_timestamp = datetime.date.today().strftime('%Y%m%d')
        self.month_count_timestamp = datetime.date.today().strftime('%Y%m')

def connect_database(sql_connection):
    engine = create_engine(sql_connection)
    Session.configure(bind=engine)

    # If table doesnt exists create it
    if engine.dialect.has_table(engine.connect(), TABLE_NAME) == False:
        Base.metadata.create_all(engine)
