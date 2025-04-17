INSERT INTO invitations (userid, movieid, text, image_urls, cinema_ids, status, amount_of_reach)
VALUES (?, ?, ?, ?, ?, ?, ?)
RETURNING *;