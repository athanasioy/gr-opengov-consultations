/*ADD legislation_type and fek_number columns to Legislation TABLE */

ALTER TABLE Legislation ADD legislation_type NVARCHAR(100);
ALTER TABLE Legislation ADD fek_number NVARCHAR(100); 