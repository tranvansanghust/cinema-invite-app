from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.movie import router as movie_router
from app.api.auth import router as auth_router
import os
from app.db import init_db  # Import the database initialization function
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
from fastapi.responses import FileResponse  # Import FileResponse

app = FastAPI()

# Mount the build directory to the root path
app.mount("/static", StaticFiles(directory="../frontend/build/static", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()  # Initialize the database on startup

app.include_router(movie_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return FileResponse("../frontend/build/index.html")

@app.get("/search")
def read_search():
    return FileResponse("../frontend/build/index.html")

@app.get("/login")
def read_login():
    return FileResponse("../frontend/build/index.html")

@app.get("/profile")
def read_profile():
    return FileResponse("../frontend/build/index.html")
