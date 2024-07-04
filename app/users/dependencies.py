from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.exceptions import TokenAbsentException, IncorrectTokenFormatException, \
    TokenExpireException, UserIsNotExistException
from app.config import settings
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY_FOR_JWT, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpireException

    user_id = int(payload.get("sub"))

    if not user_id:
        raise UserIsNotExistException 

    user = await UserDAO.get_one_or_none(id=user_id)

    if not user:
        raise UserIsNotExistException

    return user

