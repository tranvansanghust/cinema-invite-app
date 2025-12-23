import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.movie import Movie
from sqlalchemy.exc import IntegrityError

def insert_example_data():
    """
    Insert example movie data into the MySQL database.
    Uses SQLAlchemy ORM to insert data.
    """
    db = SessionLocal()
    
    try:
        # Example data for movies table
        movies_data = [
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology.',
                'release_date': '2010-07-16',
                'genre': 'Sci-Fi',
                'director': 'Christopher Nolan',
                'actors': 'Leonardo DiCaprio, Joseph Gordon-Levitt'
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns about the true nature of reality and his role in the war against its controllers.',
                'release_date': '1999-03-31',
                'genre': 'Action',
                'director': 'Lana Wachowski, Lilly Wachowski',
                'actors': 'Keanu Reeves, Laurence Fishburne'
            },
            {
                'title': 'Interstellar',
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'release_date': '2014-11-07',
                'genre': 'Adventure',
                'director': 'Christopher Nolan',
                'actors': 'Matthew McConaughey, Anne Hathaway'
            }
        ]
        
        inserted_count = 0
        skipped_count = 0
        
        for movie_data in movies_data:
            # Check if movie already exists
            existing_movie = db.query(Movie).filter(Movie.title == movie_data['title']).first()
            
            if existing_movie:
                print(f"Movie '{movie_data['title']}' already exists, skipping...")
                skipped_count += 1
                continue
            
            # Create new movie instance
            movie = Movie(**movie_data)
            db.add(movie)
            inserted_count += 1
            print(f"Inserting movie: {movie_data['title']}")
        
        # Commit all changes
        db.commit()
        print(f"\n✅ Successfully inserted {inserted_count} movies")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} movies (already exist)")
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error inserting data: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Unexpected error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting data insertion...")
    insert_example_data()
    print("Data insertion completed!")
