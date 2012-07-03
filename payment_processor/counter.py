from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import datetime

class GatewayCounter:
    day_amount_limit = None
    month_amount_limit = None
    day_trans_limit = None
    month_trans_limit = None
    _day_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
    _month_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
    _day_trans_count = [0, datetime.date.today().strftime('%Y%m')]
    _month_trans_count = [0, datetime.date.today().strftime('%Y%m')]
    _base_gateway = None

    def __init__(self, day_amount_limit=None, month_amount_limit=None,
            day_trans_limit=None, month_trans_limit=None, *args, **kwargs):
        self._base_gateway.__init__(self, *args, **kwargs)
        self.day_amount_limit = day_amount_limit
        self.month_amount_limit = month_amount_limit
        self.day_trans_limit = day_trans_limit
        self.month_trans_limit = month_trans_limit

    def _check_counts(self, day_amount_change, month_amount_change,
                   day_trans_change, month_trans_change):
        counts = self.get_counts()

        # Add change to counts
        day_amount_count = counts[0] + day_amount_change
        month_amount_count = counts[1] + month_amount_change
        day_trans_count = counts[2] + day_trans_change
        month_trans_count = counts[3] + month_trans_change

        # Check counts
        if (day_amount_count >= self.day_amount_limit and
                self.day_amount_limit != None):
            raise LimitExceeded('Gateway day amount limit reached.')

        if (month_amount_count >= self.month_amount_limit and
                self.month_amount_limit != None):
            raise LimitExceeded('Gateway month amount limit reached.')

        if (day_trans_count >= self.day_trans_limit and
                self.day_trans_limit != None):
            raise LimitExceeded('Gateway day transaction limit reached.')

        if (month_trans_count >= self.month_trans_limit and
                self.month_trans_limit != None):
            raise LimitExceeded('Gateway month transaction limit reached.')

    def _charge(self, transaction):
        # Check for transaction amount
        if transaction.amount == None:
            raise TypeError('Transaction.amount is required for ' +
                            'counter gateways.')

        # Check and increase counts
        self._check_counts(transaction.amount, transaction.amount, 1, 1)
        self.set_counts(transaction.amount, transaction.amount, 1, 1)

        try:
            return self._base_gateway._charge(self, transaction)
        except Exception:
            # Undo counts then raise exception
            self._increase_counts(-1, transaction.amount * -1)
            raise

    def _capture(self, transaction):
        # Check for transaction amount
        if transaction.amount == None:
            raise TypeError('Transaction.amount is required for ' +
                            'counter gateways.')

        # Check and increase counts
        self._check_counts(transaction.amount, transaction.amount, 1, 1)
        self.set_counts(transaction.amount, transaction.amount, 1, 1)

        try:
            return self._base_gateway._capture(self, transaction)
        except Exception:
            # Undo counts then raise exception
            self._increase_counts(-1, transaction.amount * -1)
            raise

    def get_counts(self):
        current_date = datetime.date.today()
        day_timestamp = current_date.strftime('%Y%m%d')
        month_timestamp = current_date.strftime('%Y%m')

        # If timestamp has changed reset count
        if self._day_amount_count[1] != day_timestamp:
            self._day_amount_count = [0, day_timestamp]
        if self._month_amount_count[1] != month_timestamp:
            self._month_amount_count = [0, month_timestamp]
        if self._day_trans_count[1] != day_timestamp:
            self._day_trans_count = [0, day_timestamp]
        if self._month_trans_count[1] != month_timestamp:
            self._month_trans_count = [0, month_timestamp]

        return (self._day_amount_count[0], self._month_amount_count[0],
                self._day_trans_count[0], self._month_trans_count[0])

    def set_counts(self, day_amount_change, month_amount_change,
                   day_trans_change, month_trans_change):
        current_date = datetime.date.today()

        # Increase counts
        self._day_amount_count[0] += day_amount_change
        self._month_amount_count[0] += month_amount_change
        self._day_trans_count[0] += day_trans_change
        self._month_trans_count[0] += month_trans_change

        print self._day_amount_count
        print self._month_amount_count
        print self._day_trans_count
        print self._month_trans_count

def counted_gateway(base_gateway, gateway_counter):
    class PatchedGateway(gateway_counter, base_gateway):
        _base_gateway = base_gateway

    return PatchedGateway
