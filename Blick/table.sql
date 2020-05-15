CREATE TABLE articles.blick
(
    id int NOT NULL,
    title text,
    author text[],
    published_date timestamp without time zone,
    summary text,
    content text,
    url text,
    image_url text,
    type smallint[],
    PRIMARY KEY (id)
);

ALTER TABLE articles.blick
    OWNER to vkphdmoa;

#############################
CREATE TABLE articles.feed_blick
(
    id smallint NOT NULL,
    feed text NOT NULL,
    url text NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE articles.feed_blick
    OWNER to vkphdmoa;

    ###########

INSERT INTO articles.feed_blick (id, feed, url)
VALUES
(1, 'News', 'https://www.blick.ch/news/rss.xml'),
(2, 'News/Schweiz', 'https://www.blick.ch/news/schweiz/rss.xml'),
(3, 'News/Ausland', 'https://www.blick.ch/news/ausland/rss.xml'),
(4 ,  'News/Wirtschaft' ,  'https://www.blick.ch/news/wirtschaft/rss.xml'),
(5 ,  'Sport' ,  'https://www.blick.ch/sport/rss.xml'),
(6 ,  'Sport/Fussball' ,  'https://www.blick.ch/sport/fussball/rss.xml'),
(7 ,  'Sport/Eishockey' ,  'https://www.blick.ch/sport/eishockey/rss.xml'),
(8 ,  'Sport/Ski' ,  'https://www.blick.ch/sport/ski/rss.xml'),
(9 ,  'Sport/Tennis' ,  'https://www.blick.ch/sport/tennis/rss.xml'),
(10 ,  'Sport/Formel 1' ,  'https://www.blick.ch/sport/formel1/rss.xml'),
(11 ,  'Sport/Rad' ,  'https://www.blick.ch/sport/rad/rss.xml'),
(12 ,  'People' ,  'https://www.blick.ch/people-tv/rss.xml'),
(13 ,  'Life' ,  'https://www.blick.ch/life/rss.xml'),
(14 ,  'Digital' ,  'https://www.blick.ch/digital/rss.xml')
