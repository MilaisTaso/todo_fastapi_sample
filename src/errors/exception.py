from typing import Any

from fastapi import HTTPException, status

from src.errors.messages import BaseMessage


class APIException(HTTPException):
    """実際に返す例外を定めたクラス."""


class APIException(HTTPException):
    """API例外."""

    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        error: Any,
        status_code: int = default_status_code,
        headers: dict[str, Any] | None = None,
    ) -> None:
        self.headers = headers
        try:
            error_obj = error()
        except Exception:
            error_obj = error

        try:
            message = error_obj.text.format(error_obj.param)
        except Exception:
            message = error_obj.text

        try:
            self.status_code = error_obj.status_code
        except Exception:
            self.status_code = status_code

        self.detail = {"error_code": str(error_obj), "error_msg": message}
        print(self.detail)
        super().__init__(self.status_code, self.detail, self.headers)
