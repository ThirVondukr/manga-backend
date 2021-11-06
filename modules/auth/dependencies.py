from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from db.models.users import User
from modules.auth.services import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(),
) -> User:
    return await auth_service.get_user_from_jwt(token=token)
