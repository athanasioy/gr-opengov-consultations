CREATE TABLE ArticleAnalysis (
    p_articleID int,
    p_articleNo text,
    f_articleID int,
    f_articleNo text,
    p_legislation_id int,
    days_diff int,
    diff_count int,
    similarity_ratio real,
    comments_allowed int,
    total_comments int,
    positivity_score real,
    primary key (p_articleID,f_articleID)
)
ALTER TABLE ArticleAnalysis ADD comments_allowed int;
ALTER TABLE ArticleAnalysis ADD p_articleNo text;
ALTER TABLE ArticleAnalysis ADD f_articleNo text;