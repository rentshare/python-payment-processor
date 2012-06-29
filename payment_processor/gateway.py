from payment_processor.exceptions import *
from payment_processor.transaction import Transaction
import requests

class BaseGateway:
    """Base gateway class."""
    def __init__(self, trans_limit=None):
        self._trans_amount_limit = trans_limit
        self._day_amount_limit = None
        self._month_amount_limit = None
        self._day_trans_limit = None
        self._month_trans_limit = None
        self._trans_amount_count = 0
        self._day_amount_count = 0
        self._month_amount_count = 0
        self._day_trans_count = 0
        self._month_trans_count = 0

    def _send(self, transaction, params):
        """Send transaction params with HTTP request to gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*params*", "dict", "Dictonary of HTTP parameters to send."

        Returns:
            Response from gateway.
        """
        # Send request
        try:
            response = requests.get(self._url, params=params)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Failed to connect to %r.' % self._url)

        # Check status code
        if response.status_code != requests.codes.ok:
            raise ConnectionError(('Gateway returned unsuccessful ' +
                'HTTP status code %r.') % (response.status_code))

        return self._handle_response(transaction, response.text)

    def set_transaction_limit(self, amount):
        self._trans_amount_limit = amount

    def set_limits(self, trans_amount_limit, day_amount_limit, month_amount_limit,
                day_trans_limit, month_trans_limit):
        self._trans_amount_limit = trans_amount_limit
        self._day_amount_limit = day_amount_limit
        self._month_amount_limit = month_amount_limit
        self._day_trans_limit = day_trans_limit
        self._month_trans_limit = month_trans_limit

    def set_counts(self, trans_amount_count, day_amount_count, month_amount_count,
                day_trans_count, month_trans_count):
        self._trans_amount_count = trans_amount_count
        self._day_amount_count = day_amount_count
        self._month_amount_count = month_amount_count
        self._day_trans_count = day_trans_count
        self._month_trans_count = month_trans_count

    def get_day_amount_count(self):
        return self._day_amount_count

    def get_month_amount_count(self):
        return self._month_amount_count

    def get_day_trans_count(self):
        return self._day_trans_count

    def get_month_trans_count(self):
        return self._month_trans_count

    def increase_day_amount_count(self, count):
        return self._day_amount_count + count

    def increase_month_amount_count(self, count):
        return self._month_amount_count + count

    def increase_day_trans_count(self, count):
        return self._day_trans_count + count

    def increase_month_trans_count(self, count):
        return self._month_trans_count + count

    def new_transaction(self):
        """Create a new transaction.

        Returns:

        Instance of :attr:`Transaction` that is connected to this gateway."""
        transaction = Transaction()
        transaction._gateway = self
        return transaction

class MultiGateway(BaseGateway):
    """Multi gateway class. Allows multiple gateways to be used, in the event
    that one gateway fails the next one will be used.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*args*", "class", "Instance of gateways to use."
    """
    _gateways = []
    def __init__(self, *args):
        for arg in args:
            self._gateways.append(arg)

    def new_transaction(self):
        """Create a new transaction.

        Returns:

        Instance of :attr:`Transaction` that is connected to the gateways."""
        transaction = Transaction()
        transaction._gateway = self._gateways
        return transaction
