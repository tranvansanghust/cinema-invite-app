CREATE DATABASE IF NOT EXISTS cinema_invite_db;
USE cinema_invite_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255)
);

-- Create movies table
CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    description TEXT,
    release_date VARCHAR(255),
    genre VARCHAR(255),
    director VARCHAR(255),
    actors VARCHAR(255)
);

-- Create invitations table
CREATE TABLE IF NOT EXISTS invitations (
    invitationid INT PRIMARY KEY AUTO_INCREMENT,
    userid INT NOT NULL,
    movieid INT NOT NULL,
    text TEXT,
    image_urls TEXT,
    cinema_ids TEXT,
    status VARCHAR(255),
    amount_of_reach INT,
    FOREIGN KEY (userid) REFERENCES users(id),
    FOREIGN KEY (movieid) REFERENCES movies(id)
);