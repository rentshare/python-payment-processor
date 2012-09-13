Getting Started
===============

Example authorize and capture transaction.

.. code-block:: python

    import payment_processor

    gateway = payment_processor.AuthorizeNetAIM(
            login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

    transaction = gateway.new_transaction()
    transaction.card_number = 370000000000002
    transaction.expiration_month = 1
    transaction.expiration_year = 2015
    transaction.first_name = 'First'
    transaction.last_name = 'Last'
    transaction.address = '1 First Street'
    transaction.city = 'New York'
    transaction.state = 'NY'
    transaction.zip_code = '12345'
    transaction.customer_id = 1
    transaction.description = 'Order Description'
    transaction.customer_ip = '1.1.1.1'
    transaction.amount = 19.95
    transaction.order_number = '1234-5678-90AB-CDEF'
    transaction.ship_first_name = 'First'
    transaction.ship_last_name = 'Last'
    transaction.ship_address = '1 First Street'
    transaction.ship_city = 'New York'
    transaction.ship_state = 'NY'
    transaction.ship_zip_code = '12345'
    transaction.ship_phone = '111-222-3333'
    transaction.ship_email = 'user@domain.com'
    transaction.custom_field('custom_field', 'custom_value')

    # Authorize and capture transaction
    transaction_id = transaction.charge()
    print 'transaction_id:', transaction_id


Example authorize then capture transaction. Transactions can be captured
directly from the transaction object after calling authorize or by specify a
transaction id and calling authorize.

.. code-block:: python

    import payment_processor

    gateway = payment_processor.AuthorizeNetAIM(
            login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

    transaction = gateway.new_transaction()
    transaction.card_number = 370000000000002
    transaction.expiration_month = 1
    transaction.expiration_year = 2015
    transaction.first_name = 'First'
    transaction.last_name = 'Last'
    transaction.address = '1 First Street'
    transaction.city = 'New York'
    transaction.state = 'NY'
    transaction.zip_code = '12345'
    transaction.customer_id = 1
    transaction.description = 'Order Description'
    transaction.customer_ip = '1.1.1.1'
    transaction.amount = 19.95
    transaction.order_number = '1234-5678-90AB-CDEF'
    transaction.ship_first_name = 'First'
    transaction.ship_last_name = 'Last'
    transaction.ship_address = '1 First Street'
    transaction.ship_city = 'New York'
    transaction.ship_state = 'NY'
    transaction.ship_zip_code = '12345'
    transaction.ship_phone = '111-222-3333'
    transaction.ship_email = 'user@domain.com'

    # Authorize transaction
    transaction_id = transaction.authorize()
    print 'transaction_id:', transaction_id

    # Capture a previous transaction object
    transaction.capture()

    # Capture a previous transaction using transaction id
    transaction = gateway.new_transaction()
    transaction.transaction_id = transaction_id
    transaction.capture()


Multiple gateways can also be used. The gateways will be used in the order they
are added, when one fails the next one will be used. If all gateways return an
error the transaction will fail.

.. code-block:: python

    import payment_processor

    gateway1 = payment_processor.AuthorizeNetAIM(
            login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True)

    gateway2 = payment_processor.NationalProcessing(
            login='LOGIN', trans_key='TRANSACTION_KEY')

    gateways = payment_processor.MultiGateway(gateway1, gateway2)

    transaction = gateways.new_transaction()
    transaction.card_number = 370000000000002
    transaction.expiration_month = 1
    transaction.expiration_year = 2015
    transaction.first_name = 'First'
    transaction.last_name = 'Last'
    transaction.address = '1 First Street'
    transaction.city = 'New York'
    transaction.state = 'NY'
    transaction.zip_code = '12345'
    transaction.customer_id = 1
    transaction.description = 'Order Description'
    transaction.customer_ip = '1.1.1.1'
    transaction.amount = 19.95
    transaction.order_number = '1234-5678-90AB-CDEF'
    transaction.ship_first_name = 'First'
    transaction.ship_last_name = 'Last'
    transaction.ship_address = '1 First Street'
    transaction.ship_city = 'New York'
    transaction.ship_state = 'NY'
    transaction.ship_zip_code = '12345'
    transaction.ship_phone = '111-222-3333'
    transaction.ship_email = 'user@domain.com'

    transaction_id = transaction.charge()
    print 'transaction_id:',transaction_id


If a gateway has transaction limits the counter gateway can be used to prevent
exceeding the limits. A sql gateway counter module is included that will store
the counters in an sql database. The sql gateway counter requires sqlalchemy.

.. code-block:: python

    import payment_processor

    payment_processor.connect_database('sqlite:///:memory:')

    AuthorizeNetAIMCounted = payment_processor.counted_gateway(
        payment_processor.AuthorizeNetAIM, payment_processor.SQLGatewayCounter)

    gateway = AuthorizeNetAIMCounted(
            login='LOGIN', trans_key='TRANSACTION_KEY', sandbox=True,
            day_amount_limit=10000, month_amount_limit=1000000,
            day_trans_limit=2000, month_trans_limit=30000)

    transaction = gateway.new_transaction()
    transaction.card_number = 370000000000002
    transaction.expiration_month = 1
    transaction.expiration_year = 2015
    transaction.first_name = 'First'
    transaction.last_name = 'Last'
    transaction.address = '1 First Street'
    transaction.city = 'New York'
    transaction.state = 'NY'
    transaction.zip_code = '12345'
    transaction.customer_id = 1
    transaction.description = 'Order Description'
    transaction.customer_ip = '1.1.1.1'
    transaction.amount = 19.95
    transaction.order_number = '1234-5678-90AB-CDEF'
    transaction.ship_first_name = 'First'
    transaction.ship_last_name = 'Last'
    transaction.ship_address = '1 First Street'
    transaction.ship_city = 'New York'
    transaction.ship_state = 'NY'
    transaction.ship_zip_code = '12345'
    transaction.ship_phone = '111-222-3333'
    transaction.ship_email = 'user@domain.com'

    # Authorize and capture transaction
    transaction_id = transaction.charge()
    print 'transaction_id:', transaction_id


Modules
=======

.. toctree::
   :maxdepth: 2

   init
   counter
   database
   exceptions
   gateway
   sql_counter
   transaction
   authorize_net
   national_processing
   dummy

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
