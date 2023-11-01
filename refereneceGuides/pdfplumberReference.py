import pdfplumber
from pathlib import Path
import os
import pprint
pdf_file = Path.cwd() / "pdf_files" / "891.pdf"
pdf_file2 = Path.cwd() / "pdf_files" / "1000.pdf"
cwd = os.getcwd()

# docs : https://pypi.org/project/pdfplumber/#python-library
# metrics are expressed in "points", which is 1/72 of an inch in pdfs
with pdfplumber.open(pdf_file2) as f: # Works with Path objects as well
    print(len(f.pages))
    
    p = f.pages[5]
    # x_tolerance=3 -> add space
    # y_tolerance=3 -> add new line
    # layout=false ->
    # x_density=7.25
    # y_density=7.25
    # use_text_flow = false -> mimics PDFs flow of characters (just like cursor drag highlight)

    # txt = p.extract_text()
    # print("With Defaults")
    # print(txt)
    # print("**"*40)

    # txt = p.extract_text(layout=True)  # Perserve Layout as shown in PDF
    # print("Layout=True")
    # print(txt)
    # print("**"*40)
    # crop solution: https://github.com/jsvine/pdfplumber/issues/244
    # bbox=(x0,top,x1,bottom) [(0,0) is bottom left]
    print(f"Page Width {p.width} | Page Height {p.height}")
    p = p.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
    print(set((char['fontname'], char['object_type']) for char in p.chars if char["object_type"] == "char" and "Bold" in char["fontname"] ))
    left = p.crop(  (0,
                    64,
                    0.5 * float(p.width),
                    779
                    )
                    )
    right = p.crop((0.5 * float(p.width),
                    64,
                    p.width,
                    779
                    )
                    )
    
    txt = left.extract_text()
    txt +="\n"+ right.extract_text()
    print(txt)
    print("**"*40)

    txtFile = Path(pdf_file2.stem+"_pdfplumber.txt").write_text(txt,encoding='utf-8')
    # PDF Height=842 Width = 595
    # Gimp Coords: after 63 and before 778
    # PDF Coords: TOP: 842-63=779 | Bottom = 842-778=64