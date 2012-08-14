from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import requests
import json

class Zipmark(BaseGateway):
    """Zipmark Gateway."""
    _provider = 'zipmark'

    def __init__(self, app_id, app_secret, sandbox=False):
        BaseGateway.__init__(self)

        self._app_id = app_id
        self._app_secret = app_secret
        self._url = None

        # Set base url
        if sandbox:
            self._base_url = 'https://sandbox.zipmark.com'
        else:
            self._base_url = 'https://sandbox.zipmark.com' # TODO

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

        params['customer_id'] = transaction.customer_id
        params['user_email'] = transaction.email
        params['amount_cents'] = int(transaction.amount * 100)

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

        headers = {
            'Host': 'rentshare.com', #TODO
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.com.zipmark.v1+json'}

        auth = requests.auth.HTTPDigestAuth(self._app_id, self._app_secret)

        return requests.post(self._url, headers=headers, auth=auth,
                             data=json.dumps(params))

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

        Transaction link.
        """
        response = json.loads(response)

        # TODO
        if response['status'] != 'pending':
            raise Exception('Request was unsuccessful.')

        print response # TODO testing

        return response['links'][0]['href']

    def _credit(self, transaction):
        """Credit a previous transaction.

        Arguments:

        .. csv-table::
            :header: "argument", "type", "value"
            :widths: 7, 7, 40

            "*transaction*", "class", "Instance of :attr:`Transaction`
                containing required transaction info."

        Returns:

        Transaction link.
        """
        # Get params
        params = self._get_params(transaction)
        params = {'disbursement': params}

        # Update url
        self._url = self._base_url + '/disbursements'

        return self._send(transaction, params)
