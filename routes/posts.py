from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models.postModel as models
from schemas.postSchema import PostCreate
from services.postService import get_posts, get_post_by_id
from services.postService import create_post as create_post_service
from auth.dependencies import get_current_user
from db.connection import SessionLocal
from services.userService import get_user_by_email


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    return get_posts(db)

@router.get("/posts/{post_id}")
def read_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return get_post_by_id(post_id, db)


@router.post("/posts/test")
def test_auth_only(current_user: dict = Depends(get_current_user)):
    print(f"DEBUG: Test endpoint reached WITH auth: {current_user}")
    return {"message": "Auth works in posts router!", "user": current_user}

@router.post("/posts")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    print(f"DEBUG: Entered create_post route")
    print(f"DEBUG: current_user = {current_user}")
    
    user_email = current_user["sub"]
    print(f"DEBUG: Extracting email: {user_email}")
    
    user = get_user_by_email(db, user_email)
    print(f"DEBUG: User found: {user}")
    print(f"DEBUG: User ID: {user.id if user else 'None'}")
    
    if not user:
        print(f"DEBUG: User not found, raising 404")
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"DEBUG: About to call create_post_service")
    # Pass post object and author_id separately to service
    result = create_post_service(post, user.id, db)
    print(f"DEBUG: create_post_service returned: {result}")
    return result

