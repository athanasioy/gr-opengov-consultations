ALTER TABLE Article
ADD COLUMN voted_article_id INTEGER REFERENCES Article(id);