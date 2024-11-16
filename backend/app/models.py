
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(120), nullable=False)