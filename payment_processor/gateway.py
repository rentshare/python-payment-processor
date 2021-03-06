from payment_processor.exceptions import *
from payment_processor.transaction import Transaction
import requests
import logging

class BaseGateway( object ):
    """Base gateway class."""

    def __init__(self, trans_limit=None):
        self._trans_amount_limit = trans_limit

    def _send(self, transaction, data, **kwargs):
        """Send transaction data with HTTP request to gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*data*", "dict", "Dictonary of HTTP parameters to send."

        Returns:

        Response from gateway.
        """
        # Send request
        try:
            response = self._send_request(transaction, data, **kwargs)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Failed to connect to %r.' % self._url)

        # Check status code
        if response.status_code < 200 or response.status_code > 202:
            raise ConnectionError(('Gateway returned unsuccessful ' +
                'HTTP status code %r.') % (response.status_code))

        return self._handle_response(transaction, response.text, **kwargs)

    def _send_request(self):
        """Override with method to send request to gateway. Must return
        response object."""
        raise TypeError('Send request method not implemented for gatewy.')

    def _payment_method_validator(self, transaction):
        # Check for missing variables
        if transaction.amount == None:
            raise TypeError('Missing required field transaction.amount.')

        if transaction.card_number != None:
            if transaction.expiration_month == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_month.')

            if transaction.expiration_year == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_year.')

        elif transaction.check_account_number != None:
            if transaction.check_routing_number == None:
                raise TypeError('Missing required field ' +
                        'transaction.check_routing_number.')
            if not self._valid_routing_number_checkdigit(transaction.check_routing_number):
                raise InvalidRoutingNumber('Invalid routing number.')

        else:
            raise TypeError('Missing required field transaction.card_number.')

    def _valid_routing_number_checkdigit(self, routing_number, routing_number_length=9):
        """Tests the routing number's check digit"""
        routing_number = str( routing_number ).rjust( routing_number_length, '0' )
        sum_digit = 0

        for i in range( routing_number_length - 1 ):
            n = int( routing_number[i:i+1] )
            sum_digit += n * (3,7,1)[i % 3]

        if sum_digit % 10 > 0:
            return 10 - ( sum_digit % 10 ) == int( routing_number[-1] )
        else:
            return not int( routing_number[-1] )

    def _transaction_id_validator(self, transaction):
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

    def _charge_validator(self, transaction):
        self._payment_method_validator(transaction)

    def _authorize_validator(self, transaction):
        self._payment_method_validator(transaction)

    def _capture_validator(self, transaction):
        self._transaction_id_validator(transaction)

    def _refund_validator(self, transaction):
        self._transaction_id_validator(transaction)

    def _void_validator(self, transaction):
        self._transaction_id_validator(transaction)

    def _status_validator(self, transaction):
        self._transaction_id_validator(transaction)

    def _send_transaction(self, transaction, method_name):
        """Send a transaction method by name.

        Arguments

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*method_name*", "string", "Name of transaction method."

        Returns:

        Data returned from transaction method.
        """
        # Check transaction for valid variables
        if hasattr(self, method_name + '_validator'):
            getattr(self, method_name + '_validator')(transaction)

        # Check limit
        if (transaction.amount > self._trans_amount_limit and
                self._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        method = getattr(self, method_name)
        return method(transaction)

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
    gateways = None
    _gateway_failure_handlers = None

    def __init__(self, *gateways):
        self.gateways = gateways
        self._gateway_failure_handlers = []

    def _send_transaction(self, transaction, method_name):
        """Send a transaction method by name. If a gateway fails the next
        aviable gateway will be tried.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*method_name*", "string", "Name of transaction method."

        Returns:

        Data returned from transaction method.
        """
        last_exception = None

        for gateway in self.gateways:
            # If an error occurred on previous gateway log error
            if last_exception != None:
                logging.warning('Recvied gateway error trying next ' +
                    'gateway. Exception: %r', last_exception)

            try:
                response = gateway._send_transaction( transaction, method_name )
                # The transaction was successful with this gateway so lets
                # change the transaction's gateway to be the one that processed
                # it successfully
                transaction.gateway = gateway
                return response
            except GatewayError, exception:
                # Gateway error try next gateway
                last_exception = exception

                for handler in self._gateway_failure_handlers:
                    handler( exception, gateway, transaction, method_name )

        # All gateways failed raise last exception
        if last_exception != None:
            raise last_exception
        else:
            raise TypeError('Gateway list is empty.')

    def on_gateway_failure( self, handler ):
        self._gateway_failure_handlers.append( handler )
        return handler
