from typing import Any

from starlette import status


class BaseMessage:
    """メッセージクラスのベース."""

    text: str
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, param: Any | None = None) -> None:
        self.param = param

    def __str__(self) -> str:
        return self.__class__.__name__


class ErrorMessage:
    """エラーメッセージクラス

    -----
        BaseMessagを継承することで
        Class呼び出し時にClass名がエラーコードになり、.textでエラーメッセージも取得できるため
        エラーコードと、メッセージの管理が直感的に行える。
    ----

    """

    # 共通
    class INTERNAL_SERVER_ERROR(BaseMessage):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        text = "システムエラーが発生しました、管理者に問い合わせてください"

    class FAILURE_LOGIN(BaseMessage):
        text = "ログインが失敗しました"

    class NOT_FOUND(BaseMessage):
        text = "指定の{}が存在しません"

    class ID_NOT_FOUND(BaseMessage):
        status_code = status.HTTP_404_NOT_FOUND
        text = "指定のIDは存在しません"

    # ユーザー関係
    class ALREADY_REGISTED_EMAIL(BaseMessage):
        text = "登録済のメールアドレスです"


    class INCORRECT_EMAIL_OR_PASSWORD(BaseMessage):
        status_code = status.HTTP_403_FORBIDDEN
        text = "メールアドレスまたはパスワードが正しくありません"

    class PERMISSION_ERROR(BaseMessage):
        text = "{}権限がありません"

    class CouldNotValidateCredentials(BaseMessage):
        status_code = status.HTTP_403_FORBIDDEN
        text = "ユーザー認証に失敗しました"

    class AlreadyUserDeleted(BaseMessage):
        status_code = status.HTTP_404_NOT_FOUND
        text = "すでに退会済みのユーザーです"
