ALTER TABLE Legislation
ADD Column is_public_consultation int;

UPDATE Legislation SET is_public_consultation=1
WHERE Legislation.scrap_url like '%opengov%';

UPDATE Legislation SET is_public_consultation=0
WHERE Legislation.gov_gazzete_number is not null;

