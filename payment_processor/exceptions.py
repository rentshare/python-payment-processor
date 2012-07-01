class TransactionError(Exception):
    """Execption is related to a transaction error."""

class TransactionDeclined(TransactionError):
    """The transaction was declined."""
    pass

class TransactionHeld(TransactionError):
    """Transaction was sent successfully but held for review."""
    pass

class InvalidCardNumber(TransactionError):
    """Credit card number is invalid."""
    pass

class InvalidCardExpirationDate(TransactionError):
    """Credit card expiration date is invalid."""
    pass

class InvalidCardSecurityCode(TransactionError):
    """Credit card security code is invalid."""
    pass

class InsufficientFunds(TransactionError):
    """Credit card has insufficient funds."""
    pass

class ExpiredCard(TransactionError):
    """Credit card is expired."""
    pass

class DuplicateTransaction(TransactionError):
    """The transaction was already processed."""
    pass

class InvalidBillingAddress(TransactionError):
    """Credit card billing address doesn't match or is invalid."""
    pass

class InvalidBillingZipcode(TransactionError):
    """Credit card billing zip code doesn't match or is invalid."""
    pass

class InvalidRoutingNumber(TransactionError):
    """Check routing number is invalid."""
    pass

class InvalidAccountNumber(TransactionError):
    """Check account number is invalid."""
    pass


class GatewayError(Exception):
    """Execption is related to a gateway error."""

class TransactionFailed(GatewayError):
    """Gateway failed to process transaction."""
    pass

class ConnectionError(GatewayError):
    """Unable to connect to gateway."""
    pass

class LimitExceeded(GatewayError):
    """Transaction limit for gateway has been exceeded."""
    pass
