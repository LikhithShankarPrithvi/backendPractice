
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db.connection import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String)  # You can store comma-separated tags for now