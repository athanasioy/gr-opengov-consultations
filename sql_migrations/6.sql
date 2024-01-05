CREATE TABLE ArticleEmbeddings (
    articleId int,
    vector blob,
    primary key(atricleId)
)

ALTER TABLE ArticleEmbeddings ADD COLUMN token_size int;