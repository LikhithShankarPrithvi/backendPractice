from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
def get_posts():
    return [{"id": 101, "title": "Post A"}, {"id": 102, "title": "Post B"}]

@router.post("/posts")
def create_post(post: dict):
    return {"message": "Post created", "post": post}
