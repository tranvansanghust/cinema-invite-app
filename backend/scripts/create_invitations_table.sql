CREATE TABLE invitations (
    invitationid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    movieid INTEGER NOT NULL,
    text TEXT,
    image_urls TEXT,
    cinema_ids TEXT,
    status TEXT,
    amount_of_reach INTEGER,
    FOREIGN KEY (userid) REFERENCES users (id),
    FOREIGN KEY (movieid) REFERENCES movies (id)
);