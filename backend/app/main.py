from fastapi import FastAPI
from app.api import movie_router

app = FastAPI()

app.include_router(movie_router, prefix="/api/v1")