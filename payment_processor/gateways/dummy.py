from payment_processor.exceptions import *
from payment_processor.gateway import BaseGateway
import requests

class Dummy(BaseGateway):
	def _authorize(self, transaction):
		pass
	def _charge(self, transaction):
		pass
	def _credit(self, transaction):
		pass
