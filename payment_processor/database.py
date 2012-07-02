from payment_processor.exceptions import *
import logging

# Check if sqlalchemy is isntalled
try:
    import sqlalchemy
except ImportError:
    logging.warning('SQLAlchemy not aviable, removing SQLCounter.')
    raise SQLEngineNotAviable('SQLAlchemy not aviable.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)

class CounterTable(Base):
    __tablename__ = 'payment_processor'

    id = Column(Integer, primary_key=True)
    gateway_name = Column(String)
    day_amount_count = Column(Float)
    month_amount_count = Column(Float)
    day_trans_count = Column(Integer)
    month_trans_count = Column(Integer)
    day_count_timestamp = Column(String(8))
    month_count_timestamp = Column(String(6))

    def __init__(self, gateway_name):
        self._gateway_name = gateway_name
        self.day_amount_count = 0.0
        self.month_amount_count = 0.0
        self.day_trans_count = 0
        self.month_trans_count = 0
        self.day_count_timestamp = datetime.date.today().strftime('%Y%m%d')
        self.month_count_timestamp = datetime.date.today().strftime('%Y%m')

def build_database():
    Base.metadata.create_all(engine)
