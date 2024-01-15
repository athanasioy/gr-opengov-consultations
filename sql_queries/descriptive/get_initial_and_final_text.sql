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

SELECT 	A.legislation_id,
		A.Number,
		ArticleMapping.final_legislation_article_no,
		coalesce(row_number() OVER (PARTITION by A.legislation_id,A.MaxMappedArticle order by CAST(A.number AS INT)) -1 + ArticleMapping.final_legislation_article_no, cast(A.number as int)) as joinNum
FROM (
	SELECT 	Article.legislation_id,
			Article.number,
			MAX(ArticleMapping.public_consultation_article_no) OVER (PARTITION BY Article.legislation_id,Article.number) as MaxMappedArticle
	FROM Article
	LEFT JOIN Legislation on Legislation.id = Article.legislation_id
	LEFT JOIN ArticleMapping on ArticleMapping.legislation_id = Article.legislation_id
				and Article.number >= ArticleMapping.public_consultation_article_no
	WHERE Legislation.is_public_consultation=1
) AS A
LEFT JOIN 	ArticleMapping on ArticleMapping.legislation_id = A.legislation_id
			AND ArticleMapping.public_consultation_article_no = A.MaxMappedArticle
GROUP BY A.legislation_id, A.number, A.MaxMappedArticle,ArticleMapping.final_legislation_article_no

)
AS A
ON A.legislation_id = Article.legislation_id and A.number = Article.number
LEFT JOIN Article as FinalArticles on FinalArticles.legislation_id = Legislation.final_legislation_id AND FinalArticles.number = A.JoinNum
LEFT JOIN (
	SELECT PublicConsultation .article_id, count(*) as total_comments from PublicConsultation 
	group by PublicConsultation .article_id
) as comments_count on comments_count.article_id = Article.id