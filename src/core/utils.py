from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_convert(string: str) -> str:
    return bcrypt_context.hash(string)
