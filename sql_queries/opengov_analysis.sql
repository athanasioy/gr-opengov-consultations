select Case when legislation_type is null then 'Miscellaneous' else legislation_type end as LegislationType , count(*) as cnt from Legislation
where id<=890
group by legislation_type;

/* ποια νομοσχέδια έχουν παράπανω από μία διαβουλεύσεις */

SELECT Count(*) from Legislation WHERE final_legislation_id is not null

SELECT COUNT(Distinct final_legislation_id) FROM Legislation WHERE final_legislation_id is not null
