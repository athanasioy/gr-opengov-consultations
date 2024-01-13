/* Total Consultation and Bill Rows */
SELECT count(*) FROM Legislation

/* Totals per Consultation-Bill*/
SELECT is_public_consultation, count(*) FROM Legislation
GROUP BY is_public_consultation


/* Legislation Types */
SELECT  CASE WHEN legislation_type IS NULL THEN 'Miscellaneous' ELSE legislation_type END AS LegislationType,
        count(*) AS cnt FROM Legislation
WHERE is_public_consultation=1
GROUP BY legislation_type;

/* Analysis of 'Miscellaneou' Public Consultations */
SELECT no_final_legislation_reason, COUNT(*) FROM Legislation
WHERE is_public_consultation=1
AND legislation_type IS NULL

/* Count of Articles*/
SELECT COUNT(*) FROM Article

/* Per Consultation & Voted Law */
SELECT is_public_consultation, COUNT(*) FROM Article
LEFT JOIN Legislation on Article.legislation_id = Legislation.id
group by is_public_consultation

/* Consultations */
SELECT COUNT(*) FROM PublicConsultation

/*Matched and  Not Matched Legislation Bills */
select legislation_type,no_final_legislation_reason, count(*) from legislation
where is_public_consultation=1
and legislation_type='bill'
group by legislation_type,no_final_legislation_reason

