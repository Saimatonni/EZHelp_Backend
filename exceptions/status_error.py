from fastapi import HTTPException
from typing import List, Dict
from starlette.responses import JSONResponse

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, error_messages: List[Dict[str, str]]):
        self.message = message
        self.error_messages = error_messages
        super().__init__(status_code=status_code, detail={"success": False, "message": message, "errorMessages": error_messages})

    def __str__(self):
        return self.message

    def get_body(self, *args, **kwargs) -> bytes:
        return JSONResponse(
            {"success": False, "message": self.message, "errorMessages": self.error_messages},
            status_code=self.status_code
        ).body


class NotFound(CustomHTTPException):
    def __init__(self, detail: str = "Not Found"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=404, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class BadRequest(CustomHTTPException):
    def __init__(self, detail: str = "Bad Request"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=400, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class Unauthorized(CustomHTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=401, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class Forbidden(CustomHTTPException):
    def __init__(self, detail: str = "Forbidden"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=403, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class MethodNotAllowed(CustomHTTPException):
    def __init__(self, detail: str = "Method Not Allowed"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=405, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class Conflict(CustomHTTPException):
    def __init__(self, detail: str = "Conflict"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=409, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class UnprocessableEntity(CustomHTTPException):
    def __init__(self, detail: str = "Unprocessable Entity"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=422, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message

class InternalServerError(CustomHTTPException):
    def __init__(self, detail: str = "Internal Server Error"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=500, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message
class ExtraError(CustomHTTPException):
    def __init__(self, detail: str = "Internal Server Error"):
        error_message = {"path": "", "message": detail}
        super().__init__(status_code=500, message=detail, error_messages=[error_message])

    def __str__(self):
        return self.message
