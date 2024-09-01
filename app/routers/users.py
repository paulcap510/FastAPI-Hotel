from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..database import get_db
from ..schemas import UserCreate, UserRead, Token 
from ..models import User
from ..utils.auth import hash_password, generate_sha256_hash, get_user_by_email, authenticate_user, create_access_token
import redis
from app.utils.auth import create_verification_token
from app.utils.email import send_verification_email


ACCESS_TOKEN_EXPIRE_MINUTES = 30  

router = APIRouter()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

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

    token = create_verification_token(new_user.email)
    send_verification_email(new_user.email, token)
    return new_user



@router.post("/login", response_model=Token)
async def login_with_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )    
    return {"access_token": access_token, "token_type": "bearer"}

