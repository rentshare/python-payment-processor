from payment_processor.exceptions import *

class Transaction:
    """Stores transaction information.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*gateway*", "class", "Gateway instance."
    """
    _gateway = None

    transaction_id = None
    """Transaction ID."""
    authorize_code = None
    """Authorize code."""
    amount = None
    """Total amount decimal number."""
    tax = None
    """Tax amount decimal number."""
    freight = None
    """Shipping amount decimal number."""
    tax_exempt = None
    """``True`` if transaction is tax exempt ``False`` otherwise."""
    order_number = None
    """Order number."""
    customer_id = None
    """Customer ID."""
    description = None
    """Order description."""
    customer_ip = None
    """Customer IP address."""

    first_name = None
    """Billing first name."""
    last_name = None
    """Billing last name."""
    company = None
    """Billing company name."""
    address = None
    """Billing address line one."""
    address2 = None
    """Billing address line two."""
    city = None
    """Billing city."""
    state = None
    """Billing two letter state abbreviation."""
    zip_code = None
    """Billing five digit zip code."""
    country = None
    """Billing country use US for United States."""
    phone = None
    """Billing phone number."""
    fax = None
    """Billing fax number."""
    email = None
    """Billing email address."""

    ship_first_name = None
    """Shipping first name."""
    ship_last_name = None
    """Shipping last name."""
    ship_company = None
    """Shipping company name."""
    ship_address = None
    """Shipping address line one."""
    ship_address2 = None
    """Shipping address line two."""
    ship_city = None
    """Shipping city."""
    ship_state = None
    """Shipping two letter state abbreviation."""
    ship_zip_code = None
    """Shipping five digit zip code."""
    ship_country = None
    """Shipping country use US for United States."""
    ship_phone = None
    """Shipping phone number."""
    ship_fax = None
    """Shipping fax number."""
    ship_email = None
    """Shipping email address."""

    card_number = None
    """Credit card number."""
    expiration_month = None
    """Credit card expiration month number."""
    expiration_year = None
    """Credit card expiration year number."""
    security_code = None
    """Credit card CVV security code."""

    check_account_number = None
    """Check account number."""
    check_routing_number = None
    """Check routing number."""
    check_account_type = None
    """Check account type."""
    check_holder_type = None
    """Check holder type."""
    check_number = None
    """Check number."""

    def __init__(self, gateway):
        self._gateway = gateway

    def _send_transaction(self, method_name):
        """Send a transaction method by name.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*method_name*", "string", "Name of transaction method."

        Returns:

        Data returned from transaction method.
        """
        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        method = getattr(self._gateway, method_name)
        return method(self)

    def custom_field(self, field, value):
        """Add a custom field to HTTP gateway parameters.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*field*", "string", "Name of field."
            "*value*", "string|number", "Value of field."
        """
        pass

    def charge(self):
        """Authorize and capture the transaction.

        Requires::

            Transaction.amount

            # For credit card
            Transaction.card_number
            Transaction.expiration_month
            Transaction.expiration_year

            # For check
            Transaction.check_account_number
            Transaction.check_routing_number

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize and capture transaction
            transaction_id = transaction.charge()
            print 'transaction_id:', transaction_id
        """
        # Check for missing variables
        if self.amount == None:
            raise TypeError('Missing required field transaction.amount.')

        if self.card_number != None:
            if self.expiration_month == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_month.')

            if self.expiration_year == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_year.')

        elif self.check_account_number != None:
            if self.check_routing_number == None:
                raise TypeError('Missing required field ' +
                        'transaction.check_routing_number.')

        else:
            raise TypeError('Missing required field transaction.card_number.')

        return self._send_transaction('_charge')

    def authorize(self):
        """Authorize the transaction. Transaction must be captured to complete.

        Requires::

            Transaction.amount

            # For credit card
            Transaction.card_number
            Transaction.expiration_month
            Transaction.expiration_year

            # For check
            Transaction.check_account_number
            Transaction.check_routing_number

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize transaction
            transaction_id = transaction.authorize()
            print 'transaction_id:', transaction_id
        """
        # Check for missing variables
        if self.amount == None:
            raise TypeError('Missing required field transaction.amount.')

        if self.card_number != None:
            if self.expiration_month == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_month.')

            if self.expiration_year == None:
                raise TypeError('Missing required field ' +
                        'transaction.expiration_year.')

        elif self.check_account_number != None:
            if self.check_routing_number == None:
                raise TypeError('Missing required field ' +
                        'transaction.check_routing_number.')

        else:
            raise TypeError('Missing required field transaction.card_number.')

        return self._send_transaction('_authorize')

    def capture(self):
        """Capture a previously authorized transaction.

        Requires::

            Transaction.transaction_id

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize transaction
            transaction_id = transaction.authorize()
            print 'transaction_id:', transaction_id

            # Capture transaction
            transaction = gateway.new_transaction()
            transaction.transaction_id = transaction_id
            transaction.capture()


            # Capture can also be called after authorize
            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize then capture transaction
            transaction.authorize()
            transaction_id = transaction.capture()
            print 'transaction_id:', transaction_id
        """
        # Check for missing variables
        if self.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        return self._send_transaction('_capture')

    def refund(self):
        """Refund a previous transaction.

        Requires::

            Transaction.transaction_id

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize and capture transaction
            transaction_id = transaction.charge()
            print 'transaction_id:', transaction_id

            # Refund transaction
            transaction = gateway.new_transaction()
            transaction.transaction_id = transaction_id
            transaction.refund()
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        return self._send_transaction('_refund')

    def credit(self):
        """Credit a previous transaction.

        Requires::

            Transaction.transaction_id

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize and capture transaction
            transaction_id = transaction.charge()
            print 'transaction_id:', transaction_id

            # Credit transaction
            transaction = gateway.new_transaction()
            transaction.transaction_id = transaction_id
            transaction.credit()
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        return self._send_transaction('_credit')

    def void(self):
        """Void a previous transaction.

        Requires::

            Transaction.transaction_id

        Returns:

        Transaction ID.

        Usage::

            import payment_processor

            gateway = payment_processor.AuthorizeNetAIM(
                    login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

            transaction = gateway.new_transaction()
            transaction.card_number = 370000000000002
            transaction.expiration_month = 1
            transaction.expiration_year = 2015
            transaction.first_name = 'First'
            transaction.last_name = 'Last'
            transaction.address = '1 Somewhere Ave'
            transaction.city = 'New York'
            transaction.state = 'NY'
            transaction.zip_code = '46201'
            transaction.customer_id = 1
            transaction.description = 'Order Description'
            transaction.customer_ip = '65.192.14.10'
            transaction.amount = 20.00
            transaction.order_number = '43DJ-7203-D897-SS97'
            transaction.ship_first_name = 'First'
            transaction.ship_last_name = 'Last'
            transaction.ship_address = '1 Somewhere Ave'
            transaction.ship_city = 'New York'
            transaction.ship_state = 'NY'
            transaction.ship_zip_code = '46201'
            transaction.ship_phone = '111-222-3333'
            transaction.ship_email = 'user@domain.com'

            # Authorize and capture transaction
            transaction_id = transaction.charge()
            print 'transaction_id:', transaction_id

            # Void transaction
            transaction = gateway.new_transaction()
            transaction.transaction_id = transaction_id
            transaction.void()
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        return self._send_transaction('_void')


class MultiTransaction(Transaction):
    """Stores transaction information. Subclass of Transaction used to handle
    multiple gateways.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*gateway*", "class", "Gateway instance."
    """

    def _send_transaction(self, method_name):
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
        last_exception = TypeError('Gateway list is empty.')

        for gateway in self._gateway:
            try:
                # Check limit
                if (self.amount > gateway._trans_amount_limit and
                        gateway._trans_amount_limit != None):
                    raise LimitExceeded('Transaction limit exceeded.')

                method = getattr(gateway, method_name)
                return method(self)

            except Exception, exception:
                if isinstance(exception, GatewayError) == True:
                    # Gateway error try next gateway
                    last_exception = exception
                else:
                    raise

        raise last_exception
