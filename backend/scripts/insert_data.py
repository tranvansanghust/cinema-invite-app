import sqlite3

def insert_example_data():
    connection = sqlite3.connect('../test.db')
    cursor = connection.cursor()

    # Example data for movies table
    movies = [
        (1, 'Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology.', '2010-07-16', 'Sci-Fi', 'Christopher Nolan', 'Leonardo DiCaprio, Joseph Gordon-Levitt'),
        (2, 'The Matrix', 'A computer hacker learns about the true nature of reality and his role in the war against its controllers.', '1999-03-31', 'Action', 'Lana Wachowski, Lilly Wachowski', 'Keanu Reeves, Laurence Fishburne'),
        (3, 'Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', '2014-11-07', 'Adventure', 'Christopher Nolan', 'Matthew McConaughey, Anne Hathaway')
        ]

    cursor.executemany('''
        INSERT INTO movies (id, title, description, release_date, genre, director, actors)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', movies)

    connection.commit()
    connection.close()

# ...existing code...

if __name__ == "__main__":
    insert_example_data()
    # ...existing code...
