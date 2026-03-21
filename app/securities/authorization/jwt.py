from jose import jwt
from datetime import timedelta, datetime, timezone

from app.core.config import settings


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
        self,
        data: dict,
        expired_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()

        if expired_delta:
            expire = datetime.now(timezone.utc) + expired_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encode_jwt

