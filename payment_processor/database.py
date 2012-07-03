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
"""Name of sql table for counters."""


Session = sessionmaker()
"""SQL database session."""


Base = declarative_base()
"""Base class for sql tables."""


class CounterTable(Base):
    """SQL counter table.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*provider*", "string", "Gateway provider."
    """
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    """Column ID (Primary Key)."""
    provider = Column(String)
    """Gateway provider."""
    day_amount_count = Column(Float)
    """Total amount count for day."""
    month_amount_count = Column(Float)
    """Total amount count for month."""
    day_trans_count = Column(Integer)
    """Total number of transactions for day."""
    month_trans_count = Column(Integer)
    """Total number of transactions for month."""
    day_count_timestamp = Column(String(8))
    """Timestamp of day count YYYYMMDD."""
    month_count_timestamp = Column(String(6))
    """Timestamp of month count YYYYMM."""

    def __init__(self, provider):
        self.provider = provider
        self.day_amount_count = 0.0
        self.month_amount_count = 0.0
        self.day_trans_count = 0
        self.month_trans_count = 0
        self.day_count_timestamp = datetime.date.today().strftime('%Y%m%d')
        self.month_count_timestamp = datetime.date.today().strftime('%Y%m')


def connect_database(sql_connection):
    """Connection to sql database. If table doesn't exists on database it will
    be created.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*sql_connection*", "string", "SQL alchemy dialect url."
    """
    engine = create_engine(sql_connection)
    Session.configure(bind=engine)

    # If table doesnt exists create it
    if engine.dialect.has_table(engine.connect(), TABLE_NAME) == False:
        Base.metadata.create_all(engine)
