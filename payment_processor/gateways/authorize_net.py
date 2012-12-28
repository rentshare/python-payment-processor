from payment_processor.exceptions import *
from payment_processor.constants import *
from payment_processor.gateway import BaseGateway
import requests
import xml.dom.minidom

class AuthorizeNetAIM(BaseGateway):
    """Authorize.Net AIM gateway.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*login*", "string", "Login."
        "*trans_key*", "string", "Transaction key."
        "*sandbox*", "boolean", "Optional sandbox mode. Default is `False`."
    """
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
            self._report_url = 'https://apitest.authorize.net/' + \
                'xml/v1/request.api'
        else:
            self._url = 'https://secure.authorize.net/gateway/transact.dll'
            self._report_url = 'https://api.authorize.net/xml/v1/request.api'

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
        params['x_invoice_num'] = transaction.order_number
        params['x_description'] = transaction.description

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

        params.update(transaction._custom_fields)

        return params

    def _get_report_data(self, transaction):
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
        params['login'] = self._login
        params['trans_key'] = self._trans_key

        # Order Information
        params['trans_id'] = transaction.transaction_id

        data = ('<?xml version="1.0" encoding="utf-8"?>\n' + \
            '<getTransactionDetailsRequest ' + \
            'xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">\n' + \
            '    <merchantAuthentication>\n' + \
            '        <name>{login}</name>\n' + \
            '        <transactionKey>{trans_key}</transactionKey>\n' + \
            '    </merchantAuthentication>\n' + \
            '    <transId>{trans_id}</transId>\n' + \
            '</getTransactionDetailsRequest>').format(**params)

        return data

    def _send_request(self, transaction, data, type='delim'):
        """Send request to gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*data*", "dict", "Dictonary of HTTP parameters to send or
            string containing XML data."
            "*type*", "string", "Request type."

        Returns:

        Response object.
        """
        if type == 'delim':
            # Add custom fields to params
            data = dict(data.items() + transaction._custom_fields.items())

            return requests.get(self._url, params=data)

        elif type == 'xml':
            headers = {'content-type': 'text/xml'}

            return requests.post(self._report_url, headers=headers, data=data)

        else:
            raise TypeError('Invalid response type %r.' % type)

    def _handle_response(self, transaction, response, type='delim'):
        """Handles HTTP response from gateway.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."
            "*response*", "string", "HTTP response from gateway."
            "*type*", "string", "Request type."

        Returns:

        Transaction ID.
        """
        if type == 'delim':
            self._handle_delim_response(transaction, response)

        elif type == 'xml':
            self._handle_xml_response(transaction, response)

        else:
            raise TypeError('Invalid response type %r.' % type)

    def _handle_xml_response(self, transaction, response):
        """Handles XML response from gateway.

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
        response = response.encode('utf-8')

        try:
            dom = xml.dom.minidom.parseString(response)
        except xml.parsers.expat.ExpatError:
            # Response not valid xml
            raise TransactionFailed('Invalid gateway response.')

        try:
            messages_elem = dom.firstChild.getElementsByTagName('messages')[0]
            result_code = messages_elem.getElementsByTagName(
                'resultCode')[0].firstChild.nodeValue
            message_elem = messages_elem.getElementsByTagName('message')[0]
            message_code = message_elem.getElementsByTagName(
                'code')[0].firstChild.nodeValue
            message_text = message_elem.getElementsByTagName(
                'text')[0].firstChild.nodeValue

            if result_code == 'Ok':
                pass
            elif result_code == 'Error':
                if message_code == 'E00040':
                    raise TransactionNotFound('%s: %s' % (
                        message_code, message_text))
                else:
                    raise GatewayError('%s: %s' % (
                        message_code, message_text))
            else:
                raise ConnectionError('Result code %r unkown.' % result_code)

            if dom.firstChild.tagName != 'getTransactionDetailsResponse':
                raise ConnectionError(
                    'API response format is unknown: %r' % response)

            transaction_elem = dom.firstChild.getElementsByTagName(
                'transaction')[0]

            # Set transaction details
            status = transaction_elem.getElementsByTagName(
                'transactionStatus')[0].firstChild.nodeValue

            if status == 'authorizedPendingCapture':
                transaction.status = PENDING
            elif status == 'underReview':
                transaction.status = PENDING
            elif status == 'FDSPendingReview':
                transaction.status = PENDING
            elif status == 'FDSAuthorizedPendingReview':
                transaction.status = PENDING

            elif status == 'capturedPendingSettlement':
                transaction.status = PENDING_SETTLEMENT
            elif status == 'refundPendingSettlement':
                transaction.status = PENDING_SETTLEMENT

            elif status == 'refundSettledSuccessfully':
                transaction.status = COMPLETE
            elif status == 'settledSuccessfully':
                transaction.status = COMPLETE

            elif status == 'voided':
                transaction.status = CANCELED
            elif status == 'returnedItem':
                transaction.status = CANCELED

            elif status == 'declined':
                transaction.status = FAILED
            elif status == 'expired':
                transaction.status = FAILED
            elif status == 'failedReview':
                transaction.status = FAILED
            elif status == 'communicationError':
                transaction.status = FAILED

            elif status == 'generalError':
                transaction.status = ERROR
            elif status == 'settlementError':
                transaction.status = ERROR

            else:
                transaction.status = ERROR

            transaction.transaction_id = \
                transaction_elem.getElementsByTagName(
                    'transId')[0].firstChild.nodeValue
            transaction.amount = transaction_elem.getElementsByTagName(
                'authAmount')[0].firstChild.nodeValue

            # Set billing details
            bill_to_elem = transaction_elem.getElementsByTagName(
                'billTo')[0]
            transaction.first_name = bill_to_elem.getElementsByTagName(
                'firstName')[0].firstChild.nodeValue
            transaction.last_name = bill_to_elem.getElementsByTagName(
                'lastName')[0].firstChild.nodeValue
            transaction.address = bill_to_elem.getElementsByTagName(
                'address')[0].firstChild.nodeValue
            transaction.city = bill_to_elem.getElementsByTagName(
                'city')[0].firstChild.nodeValue
            transaction.state = bill_to_elem.getElementsByTagName(
                'state')[0].firstChild.nodeValue
            transaction.zip_code = bill_to_elem.getElementsByTagName(
                'zip')[0].firstChild.nodeValue

            if len(transaction_elem.getElementsByTagName('shipTo')):
                # Set shipping details
                ship_to_elem = transaction_elem.getElementsByTagName(
                    'shipTo')[0]
                transaction.ship_first_name = \
                    ship_to_elem.getElementsByTagName(
                        'firstName')[0].firstChild.nodeValue
                transaction.ship_last_name = ship_to_elem.getElementsByTagName(
                    'lastName')[0].firstChild.nodeValue
                transaction.ship_address = ship_to_elem.getElementsByTagName(
                    'address')[0].firstChild.nodeValue
                transaction.ship_city = ship_to_elem.getElementsByTagName(
                    'city')[0].firstChild.nodeValue
                transaction.ship_state = ship_to_elem.getElementsByTagName(
                    'state')[0].firstChild.nodeValue
                transaction.ship_zip_code = ship_to_elem.getElementsByTagName(
                    'zip')[0].firstChild.nodeValue

            # Set payment method details
            payment_elem = transaction_elem.getElementsByTagName('payment')[0]

            if len(transaction_elem.getElementsByTagName('creditCard')):
                credit_card_elem = transaction_elem.getElementsByTagName(
                    'creditCard')[0]
                transaction.card_number = \
                    credit_card_elem.getElementsByTagName(
                        'cardNumber')[0].firstChild.nodeValue
                transaction.expiration_month = \
                    credit_card_elem.getElementsByTagName(
                        'expirationDate')[0].firstChild.nodeValue[:2]
                transaction.expiration_year = \
                    credit_card_elem.getElementsByTagName(
                        'expirationDate')[0].firstChild.nodeValue[2:]
                transaction.card_type = credit_card_elem.getElementsByTagName(
                    'cardType')[0].firstChild.nodeValue

            elif len(transaction_elem.getElementsByTagName('bankAccount')):
                bank_account_elem = transaction_elem.getElementsByTagName(
                    'bankAccount')[0]
                transaction.check_account_number = \
                    credit_card_elem.getElementsByTagName(
                        'accountNumber')[0].firstChild.nodeValue
                transaction.check_routing_number = \
                    credit_card_elem.getElementsByTagName(
                        'routingNumber')[0].firstChild.nodeValue[:2]
                transaction.check_account_name = \
                    credit_card_elem.getElementsByTagName(
                        'nameOnAccount')[0].firstChild.nodeValue[2:]
                transaction.check_transaction_type = \
                    credit_card_elem.getElementsByTagName(
                        'echeckType')[0].firstChild.nodeValue[2:]

        except IndexError, AttributeError:
            # Dom traversal failure
            raise ConnectionError(
                'API response format is unknown: %r' % response)

        return transaction.transaction_id

    def _handle_delim_response(self, transaction, response):
        """Handles delimited response from gateway.

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

        # Get avs response
        cc_response = response_data[38]

        # Check response code
        if response_code == 1:
            return transaction_id

        elif response_code == 4:
            raise TransactionHeld(response_reason_text)

        else:
            # Parse response reason code
            if response_reason_code in (45, 65):
                raise InvalidCardInformation(response_reason_text)

            if response_reason_code in (6, 37, 200, 315):
                raise InvalidCardNumber(response_reason_text)

            if response_reason_code in (7, 8, 202, 316, 317):
                raise InvalidCardExpirationDate(response_reason_text)

            if response_reason_code in (44, 65, 78):
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

            if response_reason_code in (4, 41, 250, 251):
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

    def _status(self, transaction):
        """Get status of a previous transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction ID.
        """
        # Get data
        data = self._get_report_data(transaction)

        return self._send(transaction, data, type='xml')
