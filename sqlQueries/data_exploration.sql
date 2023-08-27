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


 
SELECT * FROM Legislation
WHERE ministry='Επιτροπή Πληροφορικής και Επικοινωνιών'


SELECT DISTINCT ministry FROM Legislation

--	Dubious Ministries:	Open Government Partnership | Ελληνική Ραδιοφωνία Τηλεόραση Α.Ε.(ΕΡΤ ΑΕ) | Επιτροπή Προμηθειών Υγείας | Επιτροπή Πληροφορικής και Επικοινωνιών






