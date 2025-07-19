from sqlalchemy.orm import Session
from models.postModel import Post
from schemas.postSchema import PostCreate



def create_post(post: PostCreate, author_id: int, db: Session):
    db_post = Post(title=post.title, content=post.content, tags=post.tags, author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session):
    return db.query(Post).all()

def get_post_by_id(post_id: int, db: Session):
    return db.query(Post).filter(Post.id == post_id).first()
