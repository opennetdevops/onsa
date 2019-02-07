from django.http import JsonResponse
from charles.constants import *
import logging


class CustomException(Exception):

    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    def __init__(self, message, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.message = message

    def name(self):
        return str(self.__class__.__name__)

    def handle(self):
        logging.error(self)
        return JsonResponse({"msg": str(self)}, status=self.status_code)

