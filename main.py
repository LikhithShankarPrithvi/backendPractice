from fastapi import FastAPI
from routes.user import router as user_router
from routes.posts import router as posts_router
from db.connection import engine, Base

app = FastAPI()
app.include_router(user_router)
app.include_router(posts_router)

# Import all models to register them with Base
from models.userModel import User

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}