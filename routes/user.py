from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models.userModel as models
from schemas.userSchema import UserCreate, UserLogin, UserOut, TokenResponse
from auth.dependencies import get_current_user
from db.connection import SessionLocal
from services.userService import create_user, get_user_by_email
from auth.jwt import create_access_token
from auth.security import verify_password





router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"DEBUG: Attempting to register user with email: {user.email}")
    
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        print(f"DEBUG: User with email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    print(f"DEBUG: Creating new user with email: {user.email}")
    created_user = create_user(user, db)
    
    print(f"DEBUG: User created successfully with ID: {created_user.id}")
    token = create_access_token({"sub": created_user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/users/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)  # Use email for login
    
    # Debug: Check if user exists
    if not db_user:
        print(f"DEBUG: User with email {user.email} not found in database")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Debug: Check password verification
    print(f"DEBUG: Verifying password for user {db_user.email}")
    print(f"DEBUG: Plain password length: {len(user.password)}")
    print(f"DEBUG: Hashed password length: {len(db_user.password)}")
    
    password_valid = verify_password(user.password, db_user.password)
    print(f"DEBUG: Password verification result: {password_valid}")
    
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # ✅ This creates the JWT
    token = create_access_token({"sub": db_user.email})
    
    # ✅ This returns the JWT to the client
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/users/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()



@router.get("/users/me")
def read_protected_user(current_user: dict = Depends(get_current_user)):
    return current_user