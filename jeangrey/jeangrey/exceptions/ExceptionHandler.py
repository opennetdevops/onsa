from django.http import JsonResponse
from jeangrey.constants import *
import logging

class ExceptionHandler(Exception):
	def __init__(self, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
		self.status_code = status_code

	def handle(self):
		logging.error(self)
		return JsonResponse({"msg": str(self)}, status=self.status_code)