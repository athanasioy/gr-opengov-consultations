/* Top Legislaitons based on Article Count */
SELECT Legislation.title, Legislation.id, count(*) as ArticleCounts FROM Legislation
LEFT JOIN Article on article.legislation_id = Legislation.id
GROUP by Legislation.title, Legislation.id
order by 3 DESC

SELECT * from Legislation where id = 424

/* Total Legislations */
SELECT count(*) as Legislations_cnt from Legislation

/* Total Articles*/
SELECT count(*) as Articles_cnt from Article

/* Total Public Consultations*/

SELECT count(*) as PubliConsultations_cnt from PublicConsultation

/* Consultations Per Ministry */
SELECT Legislation.ministry, count(*) as PublicConsultation_cnt FROM Legislation
LEFT JOIN Article on Article.legislation_id = Legislation.id
LEFT JOIN PublicConsultation ON PublicConsultation.article_id = article.id
group by ministry
order by 2 DESC


/* Legislations Per ministry*/
SELECT Legislation.ministry, count(*) Legislations_cnt FROM Legislation
GROUP by Legislation.ministry
order by 2 DESC


/* Public Consultation per Year*/
SELECT strftime('%Y',PublicConsultation.date_reported) as year, count(*) as Consultations_cnt FROM PublicConsultation
GROUP by strftime('%Y',PublicConsultation.date_reported)


/* Top Hour People Comment*/
select strftime('%H',PublicConsultation.date_reported) as hour, count(*) as Consultations_cnt FROM PublicConsultation
GROUP by strftime('%H',PublicConsultation.date_reported)
ORDER BY 2 DESC
