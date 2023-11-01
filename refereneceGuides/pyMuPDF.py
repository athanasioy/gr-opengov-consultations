import fitz
from pathlib import Path
pdf_file = Path.cwd() / "pdf_files" / "1000.pdf"

# Get text in natural-reading order means that
# sometimes pdf is generated not in sequence.
# for example, first the body, then the header then the footer
# "normal" reading of pdf-text will result in
# 1.body
# 2.header
# 3.footer

# which may not correspond to the way the pdf is displayed.
# taken from: https://pymupdf.readthedocs.io/en/latest/recipes-text.html#how-to-extract-text-in-natural-reading-order


# The library does not work because it removes some newlines which makes it impossible to
# distinguish between article title and article body
with fitz.open(pdf_file) as f:
    # select pages
    # f.select([10])

    txt = chr(12).join([p.get_text() for p in f])
    txtFile = Path(pdf_file.stem + "_pymupdf.txt").write_text(txt, encoding='utf-8')
    for page in f:
        # get text
        # print(page.get_text())

        # get words and corresponidng bounding boxes
        # print(page.get_text("words"))
        # bbox coordinates?
        pass