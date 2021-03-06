from payment_processor.exceptions import *
import logging

class Transaction:
    """Stores transaction information.

    Arguments:

    .. csv-table::
        :header: "argument", "type", "value"
        :widths: 7, 7, 40

        "*gateway*", "class", "Gateway instance."
    """
    PERSONAL_CHECKING = 'personal_checking'
    BUSINESS_CHECKING = 'business_checking'
    PERSONAL_SAVINGS = 'personal_savings'
    BUSINESS_SAVINGS = 'business_savings'

    PPD = 'PPD'
    WEB = 'WEB'
    TEL = 'TEL'
    CCD = 'CCD'

    gateway = None
    response_info = None
    _custom_fields = None

    status = None
    """Status of the transaction"""
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
    created_date = None
    """Transaction creation date."""

    customer_id = None
    """Customer ID."""
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
    card_type = None
    """Credit card type."""

    check_account_number = None
    """Check account number."""
    check_routing_number = None
    """Check routing number."""
    check_account_type = None
    """Check account type."""
    check_bank_name = None
    """Check bank account name."""
    check_account_name = None
    """Check account customers name."""
    check_number = None
    """Check number."""
    check_transaction_type = None
    """Check transaction type."""

    def __init__(self, gateway):
        self.gateway = gateway
        self._custom_fields = {}
        self.response_info = {}

    def custom_field(self, field, value):
        """Add a custom field to HTTP gateway parameters.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*field*", "string", "Name of field."
            "*value*", "string|number", "Value of field."
        """
        self._custom_fields[field] = value

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
        return self.gateway._send_transaction(self, '_charge')

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
        return self.gateway._send_transaction(self, '_authorize')

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
        return self.gateway._send_transaction(self, '_capture')

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
        return self.gateway._send_transaction(self, '_refund')

    def credit(self):
        """Credit a previous transaction.

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
        return self.gateway._send_transaction(self, '_credit')

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
        return self.gateway._send_transaction(self, '_void')

    def status(self):
        """Get the status of a previous transaction.

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

            # Status transaction
            transaction = gateway.new_transaction()
            transaction.transaction_id = transaction_id
            transaction.status()
        """
        return self.gateway._send_transaction(self, '_status')
