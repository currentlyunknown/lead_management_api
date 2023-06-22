from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, security, status
from sqlalchemy.orm import Session

from app.models.schemas import TokenResponse, UserPayload, UserResponse
from app.services.database import get_db
from app.services.users import (authenticate_user, create_token, create_user,
                                get_current_user, get_user_by_email)

router = APIRouter(prefix="/api/users")


@router.post("", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def api_create_user(
    payload: UserPayload, db: Session = Depends(get_db)
) -> Dict[str, str]:
    db_user = await get_user_by_email(email=payload.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
        )

    user = await create_user(payload=payload, db=db)

    return await create_token(db_user=user)


@router.post("/token", response_model=TokenResponse)
async def api_generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    user = await authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return await create_token(db_user=user)


@router.get("/me", response_model=UserResponse)
async def api_get_user(
    user: UserResponse = Depends(get_current_user),
) -> Dict[str, Any]:
    return user
