ALTER TABLE Legislation
RENAME COLUMN fek_number TO gov_gazzete_number;

ALTER TABLE Legislation
ADD COLUMN law_number NVARCHAR(100);

ALTER TABLE Legislation
ADD COLUMN no_final_legislation_reason NVARCHAR(200);   