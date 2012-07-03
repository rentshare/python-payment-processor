from payment_processor.exceptions import *
from payment_processor.transaction import Transaction, MultiTransaction
import requests

class BaseGateway:
    """Base gateway class."""

    def __init__(self, trans_limit=None):
        self._trans_amount_limit = trans_limit

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
        # Add custom fields to params
        params = dict(params.items() + transaction._custom_fields.items())

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

    def new_transaction(self):
        """Create a new transaction.

        Returns:

        Instance of :attr:`Transaction` that is connected to this gateway.
        """
        transaction = Transaction(self)
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

        Instance of :attr:`Transaction` that is connected to the gateways.
        """
        transaction = MultiTransaction(self._gateways)
        return transaction
