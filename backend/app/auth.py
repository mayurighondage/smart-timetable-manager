from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

import jwt

from sqlalchemy.orm import Session

from .database import get_db

from .models import Faculty

from .security import decode_token


security = HTTPBearer()


# ==========================================================
# GET CURRENT USER
# ==========================================================

def current_user(

    credentials: HTTPAuthorizationCredentials =
        Depends(security),

    db: Session = Depends(get_db)

):

    token = credentials.credentials

    try:

        payload = decode_token(token)

        user_id = int(payload["sub"])

    except (
        jwt.InvalidTokenError,
        KeyError,
        ValueError
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.get(
        Faculty,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not user.active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    return user


# ==========================================================
# ADMIN CHECK
# ==========================================================

def require_admin(

    user: Faculty = Depends(current_user)

):

    if user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user