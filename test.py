import payment_processor
import os

# Get login and trans_key from file
with open(os.path.expanduser('~/.passwords/authorizeNet')) as file:
    login = file.readline().rstrip('\n')
    trans_key = file.readline().rstrip('\n')

gateway = payment_processor.AuthorizeNetAIM(
        login=login, trans_key=trans_key, sandbox=True)

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
#transaction_id = transaction.charge()
#print 'transaction_id:', transaction_id

# Status transaction
transaction = gateway.new_transaction()
transaction.transaction_id = '2181630452'
transaction.status()

exit(0)

payment_processor.connect_database('sqlite:///._payment_processor.sqlite')

# Get login and trans_key from file
with open(os.path.expanduser('~/.passwords/zipmark')) as file:
    app_id = file.readline().rstrip('\n')
    app_secret = file.readline().rstrip('\n')

gateway = payment_processor.Zipmark(app_id, app_secret, True)

transaction = gateway.new_transaction()
transaction.customer_id = 'abc123'
transaction.email = 'test183@example.com'
transaction.amount = 50.00

# Example zipmark credit
transaction = transaction.credit()

# Get login and trans_key from file
with open(os.path.expanduser('~/.passwords/authorizeNet')) as file:
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
transaction.custom_field('custom_field', 'custom_value')

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
