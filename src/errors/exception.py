from typing import Any
from fastapi import HTTPException, status

from src.errors.messages import BaseMessage

class APIException(HTTPException):
    """実際に返す例外を定めたクラス."""

    def __init__(
        self,
        error_obj: BaseMessage,
        headers: dict[str, Any] | None = None,
    ) -> None:
        
        #BaseMessageクラス以外は受け取らなくする（暫定）
        if not isinstance(error_obj, BaseMessage):
            raise ValueError("Error must be an instance of BaseMessage")
        
        self.headers = headers
        message: str = error_obj.text.format(error_obj.param) if error_obj.param else error_obj.text

        self.status_code = error_obj.status_code if error_obj.status_code else status.HTTP_400_BAD_REQUEST

        self.detail = {"error_code": str(error_obj), "error_msg": message}
        super().__init__(self.status_code, self.detail, self.headers)
