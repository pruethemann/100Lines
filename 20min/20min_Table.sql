CREATE TABLE articles.twentymin
(
    id int NOT NULL,
    title text,
    author text[],
    published_date timestamp without time zone,
    summary text,
    content text,
    url text,
    image_url text,
    isCommentable boolean,
    tags text[],
    import_date timestamp without time zone,
    feed_id smallint,
    html text,
    PRIMARY KEY (id)
);

ALTER TABLE articles.twentymin
    OWNER to vkphdmoa;

#############################
CREATE TABLE articles.feed_20min
(
    id smallint NOT NULL,
    feed text NOT NULL,
    url text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE articles.feed_20min
    OWNER to vkphdmoa;



INSERT INTO articles.feed_20min (id, feed, url)
VALUES
(1, 'Front', 'https://api.20min.ch/rss/view/1'),
(2, 'Schweiz', 'https://api.20min.ch/rss/view/63'),
(3, 'Ausland', 'https://api.20min.ch/rss/view/129'),
(4, 'Wirtschaft & Börse' ,  'https://api.20min.ch/rss/view/65'),
(5, 'Zürich' ,  'https://api.20min.ch/rss/view/439'),
(6, 'Bern' ,  'https://api.20min.ch/rss/view/441'),
(7, 'Basel' ,  'https://api.20min.ch/rss/view/443'),
(8, 'Zentralschweiz' ,  'https://api.20min.ch/rss/view/447'),
(9, 'Ostschweiz' ,  'https://api.20min.ch/rss/view/449'),
(10, 'Panoroma' ,  'https://api.20min.ch/rss/view/131'),
(11, 'People' ,  'https://api.20min.ch/rss/view/89'),
(12, 'Sport' ,  'https://api.20min.ch/rss/view/67'),
(13, 'Digital' ,  'https://api.20min.ch/rss/view/69'),
(14, 'Auto' ,  'https://api.20min.ch/rss/view/71'),
(15, 'Lifestyle' ,  'https://api.20min.ch/rss/view/133')
