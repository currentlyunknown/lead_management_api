from typing import Any, Dict, Union

from fastapi import Depends, HTTPException, security, status
from jose import JWTError, jwt
from passlib import hash
from sqlalchemy.orm import Session

from app.models.models import DBUser
from app.models.schemas import UserPayload, UserResponse
from app.services.database import get_db
from app.config import get_settings

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/users/token")

settings = get_settings()

key = settings.secret_key
algorithm = settings.algorithm


async def get_user_by_email(email: str, db: Session) -> DBUser:
    return db.query(DBUser).filter(DBUser.email == email).first()


async def authenticate_user(email: str, password: str, db: Session) -> Union[DBUser, bool]:
    db_user: DBUser = await get_user_by_email(db=db, email=email)

    if not db_user:
        return False

    if not db_user.verify_password(password=password):
        return False

    return db_user


async def create_token(db_user: DBUser) -> Dict[str, str]:
    user_obj: UserResponse = UserResponse.from_orm(obj=db_user)

    token: str = jwt.encode(claims=user_obj.dict(), key=key, algorithm=algorithm)

    return dict(access_token=token, token_type="bearer")


async def create_user(payload: UserPayload, db: Session) -> DBUser:
    db_user: DBUser = DBUser(
        **payload.dict(exclude={"password"}),
        hashed_password=hash.bcrypt.hash(payload.password),
    )
    db.add(instance=db_user)
    db.commit()
    db.refresh(instance=db_user)
    return db_user


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2schema),
) -> UserResponse:
    credential_exception: HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email or Password")

    try:
        payload: Any = jwt.decode(token=token, key=key, algorithms=algorithm)
        db_user: DBUser = db.query(DBUser).get(payload["id"])
        if db_user is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return UserResponse.from_orm(obj=db_user)
