/* Data Sanity Checks */

/* Legislation with same title*/
SELECT COUNT(*) FROM Legislation
WHERE title in (SELECT title FROM Legislation GROUP BY title HAVING count(*)>1)

/* 389 Duplicate Titles to Fix*/

/* Scan Data */
SELECT * FROM Legislation
WHERE title in (SELECT title FROM Legislation GROUP BY title HAVING count(*)>1)
order by 2 -- old rows 374


/* Find Duplicate Records */
SELECT * FROM Legislation
WHERE scrap_url in (SELECT scrap_url FROM Legislation GROUP BY scrap_url HAVING count(*)>1)
order by 7

/* 20 rows duplicated -> to delete the min ID */


/* Public Consulations where no commented were allowed. (47 in total) */
SELECT * FROM Legislation
where Legislation.id in (
	select Legislation.id from Legislation
	inner join Article on article.legislation_id = Legislation.id
	group by legislation_id
	having max(article.comments_allowed) = 0
)

 
SELECT * FROM Legislation
WHERE ministry='Επιτροπή Πληροφορικής και Επικοινωνιών'


SELECT DISTINCT ministry FROM Legislation

--	Dubious Ministries:	Open Government Partnership | Ελληνική Ραδιοφωνία Τηλεόραση Α.Ε.(ΕΡΤ ΑΕ) | Επιτροπή Προμηθειών Υγείας | Επιτροπή Πληροφορικής και Επικοινωνιών





