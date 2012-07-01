from payment_processor.gateway import BaseGateway
import datetime

def counter_gateway(base_gateway, day_amount_limit, month_amount_limit,
            day_trans_limit, month_trans_limit):

    class CounterGateway(base_gateway):
        _day_amount_limit = day_amount_limit
        _month_amount_limit = month_amount_limit
        _day_trans_limit = day_trans_limit
        _month_trans_limit = month_trans_limit
        _day_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
        _month_amount_count = [0, datetime.date.today().strftime('%Y%m%d')]
        _day_trans_count = [0, datetime.date.today().strftime('%Y%m')]
        _month_trans_count = [0, datetime.date.today().strftime('%Y%m')]

        def _charge(self, transaction):
            # Check for transaction amount
            if transaction.amount == None:
                raise TypeError('Transaction.amount is required for ' +
                                'counter gateways.')

            # Increase counts
            self._increase_counts(1, transaction.amount)

            try:
                return base_gateway._charge(self, transaction)
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
            self._increase_counts(1, transaction.amount)

            try:
                return base_gateway._capture(self, transaction)
            except Exception:
                # Undo counts then raise exception
                self._increase_counts(-1, transaction.amount * -1)
                raise

        def get_day_amount_count(self):
            return self._day_amount_count[0]

        def get_month_amount_count(self):
            return self._month_amount_count[0]

        def get_day_trans_count(self):
            return self._day_trans_count[0]

        def get_month_trans_count(self):
            return self._month_trans_count[0]

        def increase_day_amount_count(self, amount):
            current_date = datetime.date.today().strftime('%Y%m%d')

            # If date has changed reset count
            if self._day_amount_count[1] != current_date:
                self._day_amount_count[0] = 0

            self._day_amount_count[0] += amount
            print self._day_amount_count
            return self._day_amount_count[0]

        def increase_month_amount_count(self, amount):
            current_date = datetime.date.today().strftime('%Y%m')

            # If date has changed reset count
            if self._month_amount_count[1] != current_date:
                self._month_amount_count[0] = 0

            self._month_amount_count[0] += amount
            print self._month_amount_count
            return self._month_amount_count[0]

        def increase_day_trans_count(self, count):
            current_date = datetime.date.today().strftime('%Y%m%d')

            # If date has changed reset count
            if self._day_trans_count[1] != current_date:
                self._day_trans_count[0] = 0

            self._day_trans_count[0] += count
            print self._day_trans_count
            return self._day_trans_count[0]

        def increase_month_trans_count(self, count):
            current_date = datetime.date.today().strftime('%Y%m')

            # If date has changed reset count
            if self._month_trans_count[1] != current_date:
                self._month_trans_count[0] = 0

            self._month_trans_count[0] += count
            print self._month_trans_count
            return self._month_trans_count[0]

        def _increase_counts(self, count, amount):
            self.increase_day_amount_count(amount)
            self.increase_month_amount_count(amount)
            self.increase_day_trans_count(count)
            self.increase_month_trans_count(count)

    return CounterGateway
