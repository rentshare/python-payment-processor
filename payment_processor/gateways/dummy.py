from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway

class Dummy(BaseGateway):
    """Dummy gateway."""
    provider = 'dummy'

    def _charge(self, transaction):
        """Authorize and capture the transaction."""
        pass

    def _authorize(self, transaction):
        """Authorize the transaction."""
        pass

    def _capture(self, transaction):
        """Capture the transaction."""
        pass

    def _refund(self, transaction):
        """Refund the transaction."""
        pass

    def _credit(self, transaction):
        """Credit the transaction."""
        pass

    def _void(self, transaction):
        """Void the transaction."""
        pass
