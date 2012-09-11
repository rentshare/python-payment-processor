from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import requests

class Dummy(BaseGateway):
    provider = 'dummy'

    def _authorize( self, transaction ):
        pass
    def _charge( self, transaction ):
        pass
