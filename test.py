



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

# Authorize and capture transaction
transaction_id = transaction.charge()
print 'transaction_id:', transaction_id





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





import payment_processor

payment_processor.connect_database('sqlite:///:memory:')

AuthorizeNetAIMCounted = payment_processor.counted_gateway(
    payment_processor.AuthorizeNetAIM, payment_processor.SQLGatewayCounter)

gateway = AuthorizeNetAIMCounted(
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

# Authorize and capture transaction
transaction_id = transaction.charge()
print 'transaction_id:', transaction_id






























exit()

import payment_processor
import os

payment_processor.connect_database('sqlite:///._payment_processor.sqlite')

# Get login and trans_key from ~/.authorizeNet
with open(os.path.expanduser('~/.authorizeNet')) as file:
    login = file.readline().rstrip('\n')
    trans_key = file.readline().rstrip('\n')

AuthorizeNetAIMCounted = payment_processor.counted_gateway(
    payment_processor.AuthorizeNetAIM, payment_processor.SQLGatewayCounter)

NationalProcessingCounted = payment_processor.counted_gateway(
    payment_processor.NationalProcessing, payment_processor.SQLGatewayCounter)

gateway = AuthorizeNetAIMCounted(login=login, trans_key=trans_key,
    sandbox=True, day_trans_limit=200, month_trans_limit=1000)

gateway2 = NationalProcessingCounted(username='username', password='password')

# Authorize Capture Example
transaction = gateway.new_transaction()
transaction.card_number = 370000000000002
transaction.expiration_month = 1
transaction.expiration_year = 2014
transaction.first_name = 'First'
transaction.last_name = 'Last'
transaction.address = '1 Somewhere Ave'
transaction.city = 'New York'
transaction.state = 'NY'
transaction.zip_code = '46201'
transaction.customer_id = 1
transaction.description = 'Some Order'
transaction.customer_ip = '65.192.14.10'
transaction.amount = 20
transaction.order_number = '43DJ-7203-D897-SS97'
transaction.ship_first_name = 'First'
transaction.ship_last_name = 'Last'
transaction.ship_address = '1 Somewhere Ave'
transaction.ship_city = 'New York'
transaction.ship_state = 'NY'
transaction.ship_zip_code = '10001'
transaction.ship_phone = '222-333-4444'
transaction.ship_email = 'email@example.com'

transaction_id = transaction.charge()
print 'transaction_id:', transaction_id


# Authorize Example
transaction = gateway.new_transaction()
transaction.card_number = 370000000000002
transaction.expiration_month = 1
transaction.expiration_year = 2014
transaction.first_name = 'First'
transaction.last_name = 'Last'
transaction.address = '1 Somewhere Ave'
transaction.city = 'New York'
transaction.state = 'NY'
transaction.zip_code = '10001'
transaction.customer_id = 1
transaction.description = 'Some Order'
transaction.customer_ip = '65.192.14.10'
transaction.amount = 20
transaction.order_number = '43DJ-7203-D897-SS97'
transaction.ship_first_name = 'First'
transaction.ship_last_name = 'Last'
transaction.ship_address = '1 Somewhere Ave'
transaction.ship_city = 'New York'
transaction.ship_state = 'NY'
transaction.ship_zip_code = '10001'
transaction.ship_phone = '222-333-4444'
transaction.ship_email = 'email@example.com'

transaction_id = transaction.authorize()
print 'transaction_id:', transaction_id

# Capture Example
transaction = gateway.new_transaction()
transaction.transaction_id = transaction_id
transaction.amount = 20

transaction_id = transaction.capture()
print 'transaction_id:', transaction_id


# Multigateway example
gateways = payment_processor.MultiGateway(gateway2, gateway)

# Authorize Capture Example
transaction = gateways.new_transaction()
transaction.card_number = 370000000000002
transaction.expiration_month = 1
transaction.expiration_year = 2014
transaction.first_name = 'First'
transaction.last_name = 'Last'
transaction.address = '1 Somewhere Ave'
transaction.city = 'New York'
transaction.state = 'NY'
transaction.zip_code = '10001'
transaction.customer_id = 1
transaction.description = 'Some Order'
transaction.customer_ip = '65.192.14.10'
transaction.amount = 20
transaction.order_number = '43DJ-7203-D897-SS97'
transaction.ship_first_name = 'First'
transaction.ship_last_name = 'Last'
transaction.ship_address = '1 Somewhere Ave'
transaction.ship_city = 'New York'
transaction.ship_state = 'NY'
transaction.ship_zip_code = '10001'
transaction.ship_phone = '222-333-4444'
transaction.ship_email = 'email@example.com'

transaction_id = transaction.charge()
print 'transaction_id:',transaction_id
