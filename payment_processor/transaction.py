from payment_processor.exceptions import *

class Transaction:
    """Stores transaction information.

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

        # Authorize Transaction
        transaction_id = transaction.authorize()
        print 'transaction_id:', transaction_id

        # Capture Transaction
        transaction_id = transaction.capture()
        print 'transaction_id:', transaction_id
    """
    _gateway = None

    transaction_id = None
    authorize_code = None
    amount = None
    tax = None
    freight = None
    duty = None
    tax_exempt = None
    order_number = None
    customer_id = None
    description = None
    customer_ip = None

    first_name = None
    last_name = None
    company = None
    address = None
    address2 = None
    city = None
    state = None
    zip_code = None
    country = None
    phone = None
    fax = None
    email = None

    ship_first_name = None
    ship_last_name = None
    ship_company = None
    ship_address = None
    ship_address2 = None
    ship_city = None
    ship_state = None
    ship_zip_code = None
    ship_country = None
    ship_phone = None
    ship_fax = None
    ship_email = None

    card_number = None
    expiration_month = None
    expiration_year = None
    security_code = None

    check_account_number = None
    check_routing_number = None
    check_account_type = None
    check_holder_type = None
    check_number = None

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

        Returns:

        Transaction ID.
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

        # If list try each gateway
        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._charge(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._charge(self)

    def authorize(self):
        """Authorize the transaction. Transaction must be captured to complete.

        Returns:

        Transaction ID.
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

        # If list try each gateway
        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._authorize(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._authorize(self)

    def capture(self):
        """Capture a previously authorized transaction.

        Returns:

        Transaction ID.
        """
        # Check for missing variables
        if self.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        # If list try each gateway
        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._capture(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._capture(self)

    def refund(self):
        """Refund a previous transaction.

        Returns:

        Transaction ID.
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        # If list try each gateway
        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._refund(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._refund(self)

    def credit(self):
        """Credit a previous transaction.

        Returns:

        Transaction ID.
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        # If list try each gateway
        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._credit(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._credit(self)

    def void(self):
        """Void a previous transaction.

        Returns:

        Transaction ID.
        """
        # Check for missing variables
        if transaction.transaction_id == None:
            raise TypeError('Missing required field ' +
                        'transaction.transaction_id.')

        if isinstance(self._gateway, list) == True:
            for gateway in self._gateway:
                try:
                    # Check limit
                    if (self.amount > gateway._trans_amount_limit and
                            gateway._trans_amount_limit != None):
                        raise LimitExceeded('Transaction limit exceeded.')

                    return gateway._void(self)
                except Exception, exception:
                    if exception._type == 'gateway':
                        # Gateway error try next gateway
                        pass
                    else:
                        raise exception

        # Check limit
        if (self.amount > self._gateway._trans_amount_limit and
                self._gateway._trans_amount_limit != None):
            raise LimitExceeded('Transaction limit exceeded.')

        return self._gateway._void(self)
