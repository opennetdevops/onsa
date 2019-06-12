from django.http import JsonResponse
from worker.constants import *
import logging


class CustomException(Exception):

    status_code = CONFIG_GENERAL_ERROR

    def __init__(self, status_code=CONFIG_GENERAL_ERROR):
        self.status_code = status_code

    def name(self):
        return str(self.__class__.__name__)

    def process(self):
        logging.error(self)
        return self.status_code
