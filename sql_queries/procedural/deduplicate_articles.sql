select a.maxID,Article.* from Article
inner join (
SELECT max(id) maxID,Article.legislation_id,Article.number, Article.text from Article
where number <>999
group by Article.legislation_id,Article.number, Article.text

having count(*)>1) as a on a.legislation_id=Article.legislation_id and a.number=Article.number and a.text = Article.text
order by 5,2


SELECT min(id) maxID,Article.legislation_id,Article.number, Article.text from Article

group by Article.legislation_id,Article.number, Article.text, Article.title

select count(*) from Article

DELETE FROM Article
where id not in (
		select min(id) from Article
		group by Article.legislation_id,Article.number, Article.text, Article.title, article.comments_allowed

)