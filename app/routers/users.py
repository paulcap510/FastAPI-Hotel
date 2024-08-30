from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..database import get_db
from ..schemas import UserCreate, UserRead  # Added UserRead
from ..models import User
from ..utils.auth import hash_password, generate_sha256_hash, get_user_by_email
# from ..utils.email import send_signup_email  # Commented out for now
from fastapi.encoders import jsonable_encoder
import redis

router = APIRouter()

# Initialize Redis
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

@router.post("/register-by-email/")
async def register_by_email(
    user_input: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_email = user_input.email
    user_from_db = get_user_by_email(db, user_email)
    if user_from_db:
        raise HTTPException(
            status_code=409, detail="Email already registered."
        )
    token = generate_sha256_hash(user_email)
    redis_client.set(f"signup_token_for_{token}", user_email, ex=600)

    # for testing 
    activation_link = f"http://localhost:5173/verify-email/?token={token}"
    # html_template = """
    # <html>
    # <body>
    # <p>Thank you for registering! Please click the link below to verify your email address:</p>
    # <a href="{activation_link}">Verify Email</a>
    # </body>
    # </html>
    # """
    # html_content = html_template.format(activation_link=activation_link)
       
    # background_tasks.add_task(send_signup_email, user_email, html_content)
    
    jsonMsg = jsonable_encoder({"message": "Verification email has been sent.", "activation_link": activation_link})
    return JSONResponse(status_code=200, content=jsonMsg)



# @router.post("/register_by_email", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def register_by_email(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

#     hashed_password = hash_password(user.password.get_secret_value())
#     new_user = User(email=user.email, hashed_password=hashed_password, is_active=False)  # Initially inactive
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     # Generate verification token and send verification email
#     token = create_verification_token(new_user.email)
#     send_verification_email(new_user.email, token)

#     return {"message": "User registered. Please check your email to verify your account."}