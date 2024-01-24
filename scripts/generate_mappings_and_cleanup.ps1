
$PATH_TO_SQLITE3 = "C:\Users\aneme\Downloads\sqlite-tools-win-x64-3450000\sqlite3.exe"
C:\Users\aneme\vscode\publicConsulationScrap\.venv\Scripts\Activate.ps1

python .\scripts\generate_article_mappings.py  
python .\scripts\generate_article_mappings.py -f .\scripts\legislations_with_large_gaps_in_matching.txt -r 0

python .\scripts\populate_article_analysis.py v2

Get-Content .\sql_queries\procedural\Article_analysis_cleanup.sql -Raw | sqlite3 .\db_file.db
