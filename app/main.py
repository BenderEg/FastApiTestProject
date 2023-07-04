from fastapi import FastAPI
from .routers import users, posts, auth,votes


app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)