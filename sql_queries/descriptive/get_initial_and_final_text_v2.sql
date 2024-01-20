SELECT 	Article.id,
		Article.legislation_id,
		Article.number,
		Article.text,
		Legislation.date_posted,
		'Not Used' as joinNum,
		FinalArticles.id as final_article_id,
		FinalArticles.legislation_id as final_legislation_id,
		FinalArticles.Text as FinalText,
		FinalLegislation.date_posted as f_legislation_date_posted,
		Article.comments_allowed,
		comments_count.total_comments
FROM Article
INNER JOIN Legislation on Legislation.id = Article.legislation_id and Legislation.final_legislation_id is not NULL
LEFT JOIN Legislation as FinalLegislation on Legislation.id	= Legislation.final_legislation_id
LEFT JOIN Article as FinalArticles on FinalArticles.id = Article.voted_article_id
LEFT JOIN (
	SELECT Article.id, count(*) as total_comments
	FROM Article
	LEFT JOIN PublicConsultation on PublicConsultation.article_id = Article.id
	GROUP by Article.id
) as comments_count on comments_count.id = Article.id
where Article.number <> 999
