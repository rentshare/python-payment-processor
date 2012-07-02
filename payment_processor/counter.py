from payment_processor.gateway import BaseGateway
import datetime

class CounterGateway:
    day_amount_limit = 0
    month_amount_limit = 0
    day_trans_limit = 0
    month_trans_limit = 0
    _day_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
    _month_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
    _day_trans_count = [0, datetime.date.today().strftime('%Y%m')]
    _month_trans_count = [0, datetime.date.today().strftime('%Y%m')]
    _base_gateway = None

    def _charge(self, transaction):
        # Check for transaction amount
        if transaction.amount == None:
            raise TypeError('Transaction.amount is required for ' +
                            'counter gateways.')

        # Increase counts
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

        # Increase counts
        self.set_counts(transaction.amount, transaction.amount, 1, 1)

        try:
            return self._base_gateway._capture(self, transaction)
        except Exception:
            # Undo counts then raise exception
            self._increase_counts(-1, transaction.amount * -1)
            raise

    def get_counts(self):
        return (self._day_amount_count[0], self._month_amount_count[0],
                self._day_trans_count[0], self._month_trans_count[0])

    def set_counts(self, day_amount_change, month_amount_change,
                   day_trans_change, month_trans_change):
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

        # Increase counts
        self._day_amount_count[0] += day_amount_change
        self._month_amount_count[0] += month_amount_change
        self._day_trans_count[0] += day_trans_change
        self._month_trans_count[0] += month_trans_change

        print self._day_amount_count
        print self._month_amount_count
        print self._day_trans_count
        print self._month_trans_count

def patch_gateway(base_gateway, counter_gateway):
    class PatchedGateway(counter_gateway, base_gateway):
        _base_gateway = base_gateway

    return PatchedGateway
