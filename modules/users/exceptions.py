from modules.exceptions import BadRequestError


class EmailIsTakenError(BadRequestError):
    detail = "Email is already in use"
    code = "EMAIL_IS_TAKEN"


class UsernameIsTakenError(BadRequestError):
    detail = "Username is already in use"
    code = "USERNAME_IS_TAKEN"
