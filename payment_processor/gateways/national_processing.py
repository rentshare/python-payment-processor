from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import urlparse

class NationalProcessing(BaseGateway):
    """National Processing gateway."""
    _provider = 'national_processing'

    def __init__(self, username, password):
        BaseGateway.__init__(self)

        self._username = username
        self._password = password
        self._url = ('https://secure.nationalprocessinggateway.com/' +
                     'api/transact.php')

    def _get_params(self, transaction):
        """Get the HTTP parameters for the gateway using the transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Dictonary of HTTP parameters.
        """
        params = {}

        # Instance Specific
        params['username'] = self._username
        params['password'] = self._password

        # Transaction Specific
        params['amount'] = transaction.amount
        params['sec_code'] = 'WEB'

        if transaction.check_account_number != None:
            # Echeck Specific
            params['x_method'] = 'ECHECK'
            params['checkaba'] = transaction.check_routing_number
            params['checkaccount'] = transaction.check_account_number
            params['checkname'] = None # TODO
            params['account_holder_type'] = None # TODO
            params['account_type'] = None # TODO

        else:
            # Credit Card Specific
            params['payment'] = 'creditcard'
            params['ccnumber'] = transaction.card_number
            params['cvv'] = transaction.security_code
            if (transaction.expiration_month != None and
                    transaction.expiration_year != None):
                expiration_date = str(transaction.expiration_month).zfill(2)
                expiration_date += str(transaction.expiration_year).zfill(2)
                params['ccexp'] = expiration_date

        # Order Information
        params['orderdescription'] = transaction.description
        params['orderid'] = transaction.order_number
        params['ponumber'] = None
        params['tax'] = transaction.tax
        params['shipping'] = transaction.freight

        # Customer Information
        params['firstname'] = transaction.first_name
        params['lastname'] = transaction.last_name
        params['company'] = transaction.company
        params['address1'] = transaction.address
        params['address2'] = transaction.address2
        params['city'] = transaction.city
        params['state'] = transaction.state
        params['zip'] = transaction.zip_code
        params['country'] = transaction.country
        params['phone'] = transaction.phone
        params['fax'] = transaction.fax
        params['email'] = transaction.email
        params['ipaddress'] = transaction.customer_ip

        # Shipping Information
        params['shipping_firstname'] = transaction.ship_first_name
        params['shipping_lastname'] = transaction.ship_last_name
        params['shipping_company'] = transaction.ship_company
        params['shipping_address1'] = transaction.address
        params['shipping_address2'] = transaction.address2
        params['shipping_city'] = transaction.city
        params['shipping_state'] = transaction.state
        params['shipping_zip'] = transaction.ship_zip_code
        params['shipping_country'] = transaction.ship_country
        params['shipping_email'] = transaction.email

        return params

    def _handle_response(self, transaction, response):
        """Handles HTTP response from gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*response*", "string", "HTTP response from gateway."

        Returns:

        Transaction ID.
        """
        print response # TODO Testing

        # Parse response
        response = urlparse.parse_qs(response)

        # Get transaction id and set transaction id in transaction class
        try:
            transaction_id = response['transactionid'][0]
        except KeyError:
            transaction_id = None
        transaction.transaction_id = transaction_id

        # Get response num
        try:
            response_num = int(response['response'][0])
        except (ValueError, KeyError):
            response_num = 3

        # Get response code
        try:
            response_code = int(response['response_code'][0])
        except (ValueError, KeyError):
            response_code = None

        # Get response text
        try:
            response_text = response['responsetext'][0]
        except KeyError:
            response_text = None

        # Get avs response
        try:
            avs_response = response['avsresponse'][0]
        except KeyError:
            avs_response = None

        # Check response code
        if response_num == 1:
            return transaction_id

        elif response_num == 4:
            raise TransactionHeld(response_text)

        else:
            # Parse response reason code
            if (response_code in (220, 221, 222, 223) or
                    response_text.startswith('Invalid Credit Card Number')):
                raise InvalidCardNumber(response_text)

            if response_code in (224,):
                raise InvalidCardExpirationDate(response_text)

            if response_code in (225,):
                raise InvalidCardSecurityCode(response_text)

            if response_text.startswith('Invalid ABA number'):
                raise InvalidRoutingNumber(response_text)

            if response_code in (0,):
                raise InvalidAccountNumber(response_text)

            if avs_response in ('B', 'W', 'Z', 'P', 'L', 'N'):
                raise InvalidBillingAddress(response_text)

            if avs_response in ('A',):
                raise InvalidBillingZipcode(response_text)

            if response_code in (2, 3, 4, 41, 250, 251):
                raise TransactionFailed(response_text)

            if (response_code in (240, 250, 251, 252, 253, 260,
                                 261, 262, 263, 264)):
                raise TransactionDeclined(response_text)

            raise TransactionFailed(response_text)

        return transaction_id

    def _charge(self, transaction):
        """Authorize and capture the transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'sale'

        return self._send(transaction, params)

    def _authorize(self, transaction):
        """Authorize the transaction. Transaction must be captured to complete.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'auth'

        return self._send(transaction, params)

    def _capture(self, transaction):
        """Capture a previously authorized transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'capture'

        return self._send(transaction, params)

    def _refund(self, transaction):
        """Refund a previous transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'refund'

        return self._send(transaction, params)

    def _credit(self, transaction):
        """Credit a previous transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'credit'

        return self._send(transaction, params)

    def _void(self, transaction):
        """Void a previous transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get params
        params = self._get_params(transaction)
        params['type'] = 'void'

        return self._send(transaction, params)
