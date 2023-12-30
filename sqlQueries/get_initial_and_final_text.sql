SELECT 	Article.id,
		Article.legislation_id,
		Article.Number,
		Article.text,
		Legislation.date_posted as p_legislation_date_posted,
		A.joinNum,
		FinalArticles.id as final_article_id,
		FinalArticles.legislation_id as final_legislation_id,
		FinalArticles.Text as FinalText,
		FinalLegislation.date_posted as f_legislation_date_posted,
		Article.comments_allowed,
		comments_count.total_comments
FROM Article
INNER JOIN Legislation on Legislation.id = Article.legislation_id and Legislation.final_legislation_id is not NULL
LEFT JOIN Legislation as FinalLegislation on FinalLegislation.id = Legislation.final_legislation_id
LEFT JOIN (

SELECT 	Article.legislation_id,
		Article.number,
		max(ArticleMapping.final_legislation_article_no) as MaxFinalArticleNumberToMap,
		coalesce(row_number() OVER (PARTITION by Article.legislation_id,max(ArticleMapping.final_legislation_article_no) order by CAST(Article.number AS INT)) -1 + max(ArticleMapping.final_legislation_article_no), Article.number) as joinNum
FROM Article	
	INNER JOIN Legislation on Legislation.id = Article.legislation_id and Legislation.final_legislation_id is not NULL
	LEFT JOIN ArticleMapping ON ArticleMapping.legislation_id = Article.legislation_id and Article.number >= ArticleMapping.public_consultation_article_no
GROUP by Article.legislation_id,Article.number)
AS A
ON A.legislation_id = Article.legislation_id and A.number = Article.number
LEFT JOIN Article as FinalArticles on FinalArticles.legislation_id = Legislation.final_legislation_id AND FinalArticles.number = A.JoinNum
LEFT JOIN (
	SELECT PublicConsultation .article_id, count(*) as total_comments from PublicConsultation 
	group by PublicConsultation .article_id
) as comments_count on comments_count.article_id = Article.id