/* check for final legislations where they are not REFERENCED*/
SELECT * FROM Legislation
WHERE ID NOT IN (SELECT Legislation.final_legislation_id from Legislation WHERE final_legislation_id IS NOT NULL)
AND scrap_url like '%hellenic%';

/* Check for REFERENCES that do not exist*/
select * from Legislation a
left join Legislation b on b.id = a.final_legislation_id
where a.final_legislation_id is not null and b.id is null;