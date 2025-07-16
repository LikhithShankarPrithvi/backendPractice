from fastapi import FastAPI
from routes.user import router as user_router
from routes.posts import router as posts_router

app = FastAPI()
app.include_router(user_router)
app.include_router(posts_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}