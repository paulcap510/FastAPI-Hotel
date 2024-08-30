from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserRead
from ..models import User
from ..utils.auth import hash_password

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password.get_secret_value())
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/register_by_email", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_by_email(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password.get_secret_value())
    new_user = User(email=user.email, hashed_password=hashed_password, is_active=False)  # Initially inactive
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate verification token and send verification email
    token = create_verification_token(new_user.email)
    send_verification_email(new_user.email, token)

    return {"message": "User registered. Please check your email to verify your account."}