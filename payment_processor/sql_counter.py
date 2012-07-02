from payment_processor.counter import CounterGateway
from payment_processor.database import CounterTable
import datetime

class SQLCounterGateway(CounterGateway):
    def get_counts(self):
        return (self._day_amount_count[0], self._month_amount_count[0],
                self._day_trans_count[0], self._month_trans_count[0])

    def set_counts(self, day_amount_change, month_amount_change,
                   day_trans_change, month_trans_change):
        current_date = datetime.date.today()
        day_timestamp = current_date.strftime('%Y%m%d')
        month_timestamp = current_date.strftime('%Y%m')
