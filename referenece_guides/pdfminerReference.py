from pdfminer.high_level import extract_text, LAParams

from pathlib import Path
import pprint

# TODO: # remove "-" at the end of the line

pdf_file1 = Path.cwd() / "pdf_files" / "921.pdf"
# text = extract_text(pdf_file1)
#Candidate Pattern: Άρθρο\s*(\d)+\n(.)+ until it meets 2 new lines -> article body until Άρθρο
# Disregard ΤΜΗΜΑ


pdf_file2 = Path.cwd() / "pdf_files" / "1000.pdf"
# text = extract_text(pdf_file2)
# failed to correctly split text in two columns in άρθρο 4
params = LAParams(line_overlap=0.2)
# line_margin: how close (vertically) lines need to be to be considered in the same paragraph
# from https://github.com/pdfminer/pdfminer.six/issues/276
params = LAParams(line_margin=2,char_margin=4)  # Merge Lines more aggresive
# Solved with those params. Oh my god I love internet.
text = extract_text(pdf_file=pdf_file2,laparams=params)

print(text)
txtFile = Path(pdf_file2.stem+"_pdfminer.txt").write_text(text,encoding='utf-8')


