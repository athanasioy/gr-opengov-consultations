import glob
from pathlib import Path

def main() -> None:
    pdf_files = glob.glob(r'**\*.pdf')
    
    # pathObj = Path(pdf_files[0])
    # print(pathObj)
    # print(pathObj.exists())
    # print(pathObj.stem)

    stems = list(map(lambda x: Path(x).stem, pdf_files))
    stems = [Path(x).stem for x in pdf_files]
    
    with open('pdf_ids.txt', 'w') as f:
        f.writelines((stem+"\n" for stem in stems))
main()