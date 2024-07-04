from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class MemNotExist(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Мем с указанным id не найден"


class UserAlreadyExistException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль или почта"


class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не существует"


class IncorrectTokenFormatException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class TokenExpireException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Время действия токена истекло"


class UserIsNotExistException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь с таким id не существует"


class CannotAddMemException(BaseException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Не удалось добавить мем"


class CannotDeleteMemException(BaseException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Не удалось удалить мем"


class CannotUpdateMemException(BaseException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail = "Не удалось обновить мем"
