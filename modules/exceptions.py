from fastapi import status


class APIException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "INTERNAL_SERVER_ERROR"
    detail: str = "Internal Server Error."

    def __init__(
        self,
        detail: str = None,
        code: str = None,
        status_code: int = None,
    ):
        self.detail = detail or self.detail
        self.code = code or self.code
        self.status_code = status_code or self.status_code


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
