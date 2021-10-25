from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from db.models.users import User
from modules.users.services import UserService
from settings import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(),
) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
        user_id = payload.get("sub", None)
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return await user_service.get(user_id=user_id)
