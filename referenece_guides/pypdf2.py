import PyPDF2
from pathlib import Path

pdf_file = Path.cwd() / "pdf_files" / "891.pdf"

#read a pdf file

with open(pdf_file,'rb') as f:
    reader = PyPDF2.PdfReader(f)
    # reading txt has to be done inside the open file

    page = reader.pages[1]
    txt = page.extract_text(" ", " ")

    print(txt)
    with open('pypdf2.txt','w', encoding='utf-8') as f2:
        f2.write(txt)
    # extract text with vertical orientation
    # 0 ->normal (turned up)
    # 90 -> turned left text
    # 180 -> upside down text
    # 270 -> turned right text
    # txt = page.extract_text()
    # txt = page.extract_text((0,90))  # For up and turned left text


    # more arguments for extract_text()
    # space_width = 200 force default space width if not extracted from font


