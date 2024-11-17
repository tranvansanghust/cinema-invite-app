from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    description: str
    release_date: str
    genre: str
    director: str
    actors: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True