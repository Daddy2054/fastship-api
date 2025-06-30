from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt

from app.config import security_settings
from uuid import uuid4

def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(days=7),
    #expiry: timedelta = timedelta(seconds=15),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired access token",
        )
    except jwt.PyJWTError:
        return None
