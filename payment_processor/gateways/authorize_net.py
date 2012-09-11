from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import requests

class AuthorizeNetAIM(BaseGateway):
    """Authorize.Net AIM gateway."""

    provider = 'authorize_net'

    def __init__(self, login, trans_key, sandbox=False, test_requests=False,
                 *args, **kwargs):
        BaseGateway.__init__(self, *args, **kwargs)

        self._login = login
        self._trans_key = trans_key
        self._sandbox = sandbox
        self._test_requests = test_requests
        self._delim_char = '|'

        # Set url
        if sandbox:
            self._url = 'https://test.authorize.net/gateway/transact.dll'
        else:
            self._url = 'https://secure.authorize.net/gateway/transact.dll'

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

        # Global
        params['x_version'] = '3.1'
        params['x_delim_data'] = 'TRUE'
        params['x_delim_char'] = self._delim_char
        params['x_encap_char'] = ''
        params['x_relay_response'] = 'FALSE'
        params['x_duplicate_window'] = '120'
        if self._test_requests == True:
            params['x_test_request'] = 'TRUE'

        # Instance Specific
        params['x_login'] = self._login
        params['x_tran_key'] = self._trans_key
        params['x_test_request'] = 'FALSE'

        # Order Information
        params['x_trans_id'] = transaction.transaction_id
        params['x_invoice_num'] = None
        params['x_description'] = None

        # Transaction Specific
        params['x_amount'] = transaction.amount

        if transaction.check_account_number != None:
            if transaction.check_account_type == transaction.PERSONAL_CHECKING:
                params['x_echeck_type'] = 'CHECKING'
            if transaction.check_account_type == transaction.BUSINESS_CHECKING:
                params['x_echeck_type'] = 'BUSINESSCHECKING'
            if transaction.check_account_type == transaction.PERSONAL_SAVINGS:
                params['x_echeck_type'] = 'SAVINGS'
            if transaction.check_account_type == transaction.BUSINESS_SAVINGS:
                params['x_echeck_type'] = 'SAVINGS'

            # Echeck Specific
            params['x_method'] = 'ECHECK'
            params['x_bank_aba_code'] = transaction.check_routing_number
            params['x_bank_acct_num'] = transaction.check_account_number
            params['x_bank_name'] = transaction.check_bank_name
            params['x_bank_acct_name'] = transaction.check_account_name
            params['x_bank_check_number'] = transaction.check_number
            params['x_echeck_type'] = transaction.check_transaction_type

        else:
            # Credit Card Specific
            params['x_method'] = 'CC'
            params['x_card_num'] = transaction.card_number
            params['x_card_code'] = transaction.security_code
            if (transaction.expiration_month != None and
                    transaction.expiration_year != None):
                expiration_date = str(transaction.expiration_month).zfill(2)
                expiration_date += str(transaction.expiration_year).zfill(2)
                params['x_exp_date'] = expiration_date

        # Customer Information
        params['x_first_name'] = transaction.first_name
        params['x_last_name'] = transaction.last_name
        params['x_company'] = transaction.company
        params['x_address'] = transaction.address
        if transaction.address2 != None:
            params['x_address'] += ', ' + transaction.address2
        params['x_city'] = transaction.city
        params['x_state'] = transaction.state
        params['x_zip'] = transaction.zip_code
        params['x_country'] = transaction.country
        params['x_phone'] = transaction.phone
        params['x_fax'] = transaction.fax
        params['x_email'] = transaction.email
        params['x_cust_id'] = transaction.customer_id
        params['x_customer_ip'] = transaction.customer_ip

        # Shipping Information
        params['x_ship_to_first_name'] = transaction.ship_first_name
        params['x_ship_to_last_name'] = transaction.ship_last_name
        params['x_ship_to_company'] = transaction.ship_company
        params['x_ship_to_address'] = transaction.ship_address
        if transaction.ship_address2 != None:
            params['x_ship_to_address'] += ', ' + transaction.ship_address2
        params['x_ship_to_city'] = transaction.ship_city
        params['x_ship_to_state'] = transaction.ship_state
        params['x_ship_to_zip'] = transaction.ship_zip_code
        params['x_ship_to_country'] = transaction.ship_country
        params['x_tax'] = transaction.tax
        params['x_freight'] = transaction.freight
        if transaction.tax_exempt == True:
            params['x_tax_exempt'] = 'TRUE'

        # Remove empty params
        for key in params.keys():
            if params[key] == None:
                del params[key]

        return params

    def _send_request(self, transaction, params):
        """Send request to gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*params*", "dict", "Dictonary of HTTP parameters to send."

        Returns:

        Response object.
        """
        # Add custom fields to params
        params = dict(params.items() + transaction._custom_fields.items())

        return requests.get(self._url, params=params)

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
        # Response
        #  0 - Response Code:
        #      1 = Approved, 2 = Declined, 3 = Error, 4 = Held for Review
        #  1 - Response Subcode
        #  2 - Response Reason Code
        #  3 - Response Reason Text
        #  4 - Authorization Code
        #  5 - AVS Response
        #  6 - Transaction ID
        #  7 - Invoice Number
        #  8 - Description
        #  9 - Amount
        # 10 - Method
        # 11 - Transaction Type
        # 12 - Customer ID
        # 13 - First Name
        # 14 - Last Name
        # 15 - Company
        # 16 - Address
        # 17 - City
        # 18 - Sate
        # 19 - Zip
        # 20 - Country
        # 21 - Phone
        # 22 - Fax
        # 23 - Email
        # 24 - Ship First Name
        # 25 - Ship Last Name
        # 26 - Ship Company
        # 27 - Ship Address
        # 28 - Ship City
        # 29 - Ship State
        # 30 - Ship Zip
        # 31 - Ship Country
        # 32 - Tax
        # 33 - Duty
        # 34 - Freight
        # 35 - Tax Exempt
        # 36 - Purchase Order Number
        # 37 - MD5 Hash
        # 38 - CCV Response
        # 39 - CAVV Response
        # 40 - Account Number
        # 41 - Card Type
        # 42 - Split Tender ID
        # 43 - Requested Amount
        # 44 - Balance on Card
        response_data = response.split(self._delim_char)

        # Check that response data is valid
        if len(response_data) < 7:
            raise TransactionFailed('Invalid gateway response.')

        # Get transaction id and set transaction id in transaction class
        transaction_id = response_data[6]
        transaction.transaction_id = transaction_id

        # Get response code
        try:
            response_code = int(response_data[0])
        except ValueError:
            response_code = 3

        # Get response reason code
        try:
            response_reason_code = int(response_data[2])
        except ValueError:
            response_reason_code = None

        # Get response reason text
        response_reason_text = response_data[3]

        # Get avs response
        avs_response = response_data[5]

        # Check response code
        if response_code == 1:
            return transaction_id

        elif response_code == 4:
            raise TransactionHeld(response_reason_text)

        else:
            # Parse response reason code
            if response_reason_code in (6, 37, 200, 315):
                raise InvalidCardNumber(response_reason_text)

            if response_reason_code in (7, 8, 202, 316, 317):
                raise InvalidCardExpirationDate(response_reason_text)

            if response_reason_code in (44, 45, 65):
                raise InvalidCardSecurityCode(response_reason_text)

            if response_reason_code in (9,):
                raise InvalidRoutingNumber(response_reason_text)

            if response_reason_code in (10,):
                raise InvalidAccountNumber(response_reason_text)

            if response_reason_code in (27, 127, 290):
                if avs_response == 'A':
                    raise InvalidBillingZipcode(response_reason_text)
                else:
                    raise InvalidBillingAddress(response_reason_text)

            if response_reason_code in (2, 3, 4, 41, 250, 251):
                raise TransactionFailed(response_reason_text)

            if response_reason_code in (11, 222, 318):
                raise DuplicateTransaction(response_reason_text)

            if response_code == 2:
                raise TransactionDeclined(response_reason_text)

            else:
                raise TransactionFailed(response_reason_text)

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
        params['x_type'] = 'AUTH_CAPTURE'

        # Send params
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
        params['x_type'] = 'AUTH_ONLY'

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
        params['x_type'] = 'PRIOR_AUTH_CAPTURE'

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
        return self._credit(transaction)

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
        params = self._get_params(transaction)
        params['x_type'] = 'CREDIT'

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
        params['x_type'] = 'VOID'

        return self._send(transaction, params)
