
from sqlalchemy.orm import Session
from app.schemas.movie import MovieCreate, Movie
from app.models.movie import Movie as MovieModel

def get_movie(db: Session, movie_id: int):
    return db.query(MovieModel).filter(MovieModel.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MovieModel).offset(skip).limit(limit).all()

def create_movie(db: Session, movie: MovieCreate):
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie