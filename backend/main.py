from fastapi import FastAPI
from app.api.movie import router as movie_router

app = FastAPI()

app.include_router(movie_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}