from modules.exceptions import UnauthorizedError


class InvalidCredentialsError(UnauthorizedError):
    detail = "Provided credentials are invalid"
    code = "INVALID_CREDENTIALS"
