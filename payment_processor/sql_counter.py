from payment_processor.exceptions import *
from payment_processor.counter import GatewayCounter
from payment_processor.database import CounterTable, Session
from sqlalchemy.exc import *
import datetime

class SQLGatewayCounter(GatewayCounter):
    """Counter gateway that uses sql to store counters."""

    def __init__(self, *args, **kwargs):
        GatewayCounter.__init__(self, *args, **kwargs)

        # If gateway column doesnt exists create it
        session = Session()
        gateway_column = session.query(CounterTable).filter(
                        CounterTable.provider == self._provider).first()
        if gateway_column == None:
            self._create_column()

    def _create_column(self):
        """Create required column for gateway counters. This is called if
        gateway column doesn't exists in database."""
        current_date = datetime.date.today()
        session = Session()

        # Create authorize net column
        authorize_net = CounterTable(self._provider)
        authorize_net.day_amount_count = 0.0
        authorize_net.month_amount_count = 0.0
        authorize_net.day_trans_count = 0
        authorize_net.month_trans_count = 0
        authorize_net.day_count_timestamp = current_date.strftime('%Y%m%d')
        authorize_net.month_count_timestamp = current_date.strftime('%Y%m')
        session.add(authorize_net)

        session.commit()

    def get_counts(self):
        """Get counts from sql database."""
        session = Session()
        current_date = datetime.date.today()
        day_timestamp = current_date.strftime('%Y%m%d')
        month_timestamp = current_date.strftime('%Y%m')

        # Get gateway conuter data
        try:
            gateway_data = session.query(CounterTable).filter(
                            CounterTable.provider == self._provider).first()
        except SQLAlchemyError, exception:
            raise CounterError(exception)

        # If timestamp has changed reset count
        if gateway_data.day_count_timestamp != day_timestamp:
            gateway_data.day_amount_count = 0.0
            gateway_data.day_trans_count = 0
            gateway_data.day_count_timestamp = day_timestamp
            try:
                session.commit()
            except SQLAlchemyError, exception:
                raise CounterError(exception)

        if gateway_data.month_count_timestamp != month_timestamp:
            gateway_data.month_amount_count = 0.0
            gateway_data.month_trans_count = 0
            gateway_data.month_count_timestamp = month_timestamp
            try:
                session.commit()
            except SQLAlchemyError, exception:
                raise CounterError(exception)

        return (gateway_data.day_amount_count, gateway_data.month_amount_count,
                gateway_data.day_trans_count, gateway_data.month_trans_count)

    def set_counts(self, day_amount_change, month_amount_change,
                   day_trans_change, month_trans_change):
        """Set counts in sql database."""
        session = Session()

        # Get gateway conuter data
        gateway_data = session.query(CounterTable).filter(
                        CounterTable.provider == self._provider).first()

        # Increase counts
        gateway_data.day_amount_count += day_amount_change
        gateway_data.month_amount_count += month_amount_change
        gateway_data.day_trans_count += day_trans_change
        gateway_data.month_trans_count += month_trans_change
        session.commit()
