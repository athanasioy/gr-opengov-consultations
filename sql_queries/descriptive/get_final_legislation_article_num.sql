 Select
		Article.Number,
		Article.legislation_id,
		map.MaxArticleToMap,
		FinalArticle.text,
		--FinaLegislationArticles.Number as FinalArtNumber,
		coalesce(row_number() OVER (PARTITION by Article.legislation_id,map.MaxArticleToMap order by CAST(Article.number AS INT)) -1 + map.MaxArticleToMap, Article.number) as joinNum
		
 FROM Article
 left join Legislation on Legislation.id = Article.legislation_id
 left join (
	SELECT 	Article.legislation_id,
			Article.number,
			max(ArticleMapping.final_legislation_article_no) as MaxArticleToMap
	FROM Article
	LEFT JOIN ArticleMapping on ArticleMapping.legislation_id = Article.legislation_id
							AND Article.number >= ArticleMapping.public_consultation_article_no
	GROUP BY 	Article.legislation_id,
				Article.number
 
 ) as map on map.legislation_id = Article.legislation_id and map.number=Article.number
 LEFT JOIN Article as FinalArticle on 	FinalArticle.legislation_id = Legislation.final_legislation_id
										--AND FinalArticle.number = coalesce(row_number() OVER (PARTITION by Article.legislation_id,map.MaxArticleToMap order by CAST(Article.number AS INT)) -1 + map.MaxArticleToMap, Article.number)

												