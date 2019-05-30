from charles.exceptions.CustomException import CustomException


class InvalidParametersException(CustomException):
    """ Raised when there is an issue gathering parameters to form dict to send to workers """
