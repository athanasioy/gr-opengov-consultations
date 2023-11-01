# Get Files with Missing Articles
Get-Content .\pdf_extract.log | Select-String -Pattern "file=pdf_files/text\\(\d+)_.*?Missing" -AllMatches | ForEach-Object {$_.Matches.Groups[1].Value} | Set-Clipboard

# Get Files with Zero Matches 
Get-Content .\pdf_extract.log | Select-String -Pattern "file=pdf_files/text\\(\d+)_.*?Empty Sequence" -AllMatches | ForEach-Object {$_.Matches.Groups[1].Value} | Set-Clipboard