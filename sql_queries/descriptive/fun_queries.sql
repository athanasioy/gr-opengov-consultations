select reporter, article.title ,count(*) from PublicConsulation
left join Article on Article.id = PublicConsulation.article_id
group by reporter, article.title
order by count(*) desc

select *, Legislation.scrap_url from PublicConsulation
left join article on Article.id = PublicConsulation.article_id
left join Legislation on Legislation.id = Article.legislation_id
where reporter="Μαρία"
and article_id=398
order by date_reported

select Legislation.title, article.title ,count(*) from Legislation
left join Article on Article.legislation_id = Legislation.id
left join PublicConsulation on PublicConsulation.article_id = Article.id
group by Legislation.title, Article.title
order by 3 desc