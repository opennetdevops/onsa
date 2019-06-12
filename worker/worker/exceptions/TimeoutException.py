from worker.exceptions.CustomException import CustomException
from worker.constants import *


class TimeoutException(CustomException):
    """Raised when there is a timeout error """
    status_code = CONFIG_TIMEOUT_ERROR
