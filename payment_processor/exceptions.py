class TransactionError(Exception):
    """Execption is related to a transaction error."""

class TransactionDeclined(TransactionError):
    """The transaction was declined."""

class TransactionHeld(TransactionError):
    """Transaction was sent successfully but held for review."""

class InvalidCardInformation(TransactionError):
    """Credit card information is invalid."""

class InvalidCardNumber(TransactionError):
    """Credit card number is invalid."""

class InvalidCardExpirationDate(TransactionError):
    """Credit card expiration date is invalid."""

class InvalidCardSecurityCode(TransactionError):
    """Credit card security code is invalid."""

class InsufficientFunds(TransactionError):
    """Credit card has insufficient funds."""

class ExpiredCard(TransactionError):
    """Credit card is expired."""

class DuplicateTransaction(TransactionError):
    """The transaction was already processed."""

class InvalidBillingAddress(TransactionError):
    """Credit card billing address doesn't match or is invalid."""

class InvalidBillingZipcode(TransactionError):
    """Credit card billing zip code doesn't match or is invalid."""

class InvalidRoutingNumber(TransactionError):
    """Check routing number is invalid."""

class InvalidAccountNumber(TransactionError):
    """Check account number is invalid."""


class GatewayError(Exception):
    """Execption is related to a gateway error."""

class TransactionFailed(GatewayError):
    """Gateway failed to process transaction."""

class TransactionNotFound(GatewayError):
    """Transaction not found."""

class ConnectionError(GatewayError):
    """Unable to connect to gateway."""

class LimitExceeded(GatewayError):
    """Transaction limit for gateway has been exceeded."""

class CounterError(GatewayError):
    """An error occurred when handling counters."""


class SQLEngineNotAviable(Exception):
    """Optional SQL engine is not aviable."""
