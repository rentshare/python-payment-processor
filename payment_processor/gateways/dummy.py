from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import random

class Dummy(BaseGateway):
    """Dummy gateway."""
    provider = 'dummy'

    def _rand_id(self):
        return str(int(random.random()*1000000))

    def _charge(self, transaction):
        """Authorize and capture the transaction."""
        return self._rand_id()

    def _authorize(self, transaction):
        """Authorize the transaction."""
        return self._rand_id()

    def _capture(self, transaction):
        """Capture the transaction."""
        return transaction.transaction_id

    def _refund(self, transaction):
        """Refund the transaction."""
        return self._rand_id()

    def _credit(self, transaction):
        """Credit the transaction."""
        return self._rand_id()

    def _void(self, transaction):
        """Void the transaction."""
        return transaction.transaction_id
