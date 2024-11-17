
from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.schemas.movie import MovieCreate

def get_movie(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Movie).offset(skip).limit(limit).all()

def create_movie(db: Session, movie: MovieCreate):
    db_movie = Movie(title=movie.title, description=movie.description)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie