from worker.exceptions.CustomException import CustomException
from worker.constants import *


class AuthException(CustomException):
    """Raised when there is an issue configuring """
    status_code = CONFIG_AUTH_ERROR
