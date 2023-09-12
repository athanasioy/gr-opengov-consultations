import re
from pathlib import Path
def main() -> None:
    log = Path("final_legislations.log")
    
    if not log.exists():
        raise NameError("Log File does not exist!")
    txt = log.read_text()
    pattern = r"Multiple results returned for (\d+)"

    objsWithMultipleResults = re.findall(pattern,txt)

    objs = [int(obj) for obj in objsWithMultipleResults]
    objs = set(objs)
    
    

main()

