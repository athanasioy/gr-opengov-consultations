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
