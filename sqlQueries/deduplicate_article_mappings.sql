/* NULL VALUES INDICATE DUPLICATES*/
select * from ArticleMapping a 
left join (
select 	min(ArticleMapping.id) as minID,
		legislation_id,
		ArticleMapping.final_legislation_article_no,
		public_consultation_article_no,
		count(*) as cnt
from ArticleMapping
group by legislation_id,public_consultation_article_no,final_legislation_article_no
--having count(*)>1
) as b on b.minID = a.id
order by 2,1

--SELECT *
DELETE
FROM ArticleMapping
where id not in (
	/*Deduplicate Table ArticleMapping based on legislation_id,public_consultation_article_no,final_legislation_article_no */
	select 	min(ArticleMapping.id) as minID
	from ArticleMapping
	group by legislation_id,public_consultation_article_no,final_legislation_article_no

)



