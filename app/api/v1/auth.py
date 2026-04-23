from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.services.auth_service import create_user, authenticate_user, get_user_by_email
from app.schemas.auth import UserRegister, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(400, "Password do not match")
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(400, "Email aleready registered")
    db_user = create_user(db, user.email, user.password)
    return {"message": "User created", "email": db_user.email}


@router.post("/login", response_model=Token)
def loign(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token}
