from pydantic_core import PydanticCustomError

class NotFoundError(PydanticCustomError):
    def __new__(cls, msg: str):
        return PydanticCustomError.__new__(cls, "not_found", "{msg}", {"msg": msg})
    def __init__(self, msg: str):
        pass

class UnauthorizedError(PydanticCustomError):
    def __new__(cls, msg: str):
        return PydanticCustomError.__new__(cls, "unauthorized_error", "{msg}", {"msg": msg})
    def __init__(self, msg: str):
        pass

class ForbiddenError(PydanticCustomError):
    def __new__(cls, msg: str):
        return PydanticCustomError.__new__(cls, "forbidden_error", "{msg}", {"msg": msg})
    def __init__(self, msg: str):
        pass