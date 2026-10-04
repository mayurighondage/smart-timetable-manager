from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Faculty
from ..schemas import LoginRequest, TokenResponse
from ..security import (
    verify_password,
    create_access_token
)
from ..auth import current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================================
# LOGIN
# ==========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(
        Faculty
    ).filter(
        Faculty.email == data.email
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    token = create_access_token(
        user.id,
        user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ==========================================================
# CURRENT USER
# ==========================================================

@router.get("/me")
def get_me(
    user=Depends(current_user)
):

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "expertise": [
            x.strip()
            for x in user.expertise.split(",")
            if x.strip()
        ]
    }