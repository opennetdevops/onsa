from django.http import JsonResponse
from core.constants import *
import logging

class CustomException(Exception):

    status_code=HTTP_500_INTERNAL_SERVER_ERROR
    
    def __init__(self, message, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.message = message

    def handle(self):
        logging.error(self)
        logging.error(str("error code: " + str(self.status_code)))
        return JsonResponse({"msg": str(self)}, status=int(self.status_code))

    def handleAsJson(self):
        logging.error(self)
        return JsonResponse({"msg": str(self)}, status=int(self.status_code))