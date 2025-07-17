from sqlalchemy.orm import Session
from models.userModel import User
from schemas.userSchema import UserCreate
from auth.security import hash_password

def create_user(user: UserCreate, db: Session):
    # Debug: Check password before hashing
    print(f"DEBUG: Original password: {user.password}")
    print(f"DEBUG: Original password length: {len(user.password)}")
    
    hashed_password = hash_password(user.password)
    
    # Debug: Check password after hashing
    print(f"DEBUG: Hashed password: {hashed_password}")
    print(f"DEBUG: Hashed password length: {len(hashed_password)}")
    
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()