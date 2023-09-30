from pathlib import Path
import re

def main() -> None:
    log = Path.cwd() / "final_legislations.log"
    if not log.exists():
        raise ValueError("Log Does not exist!")
    
    pattern = r"Did not find legislation for legObj with id=(\d+)"

    text = log.read_text()

    matches = re.findall(pattern,text)

    objs = [int(x) for x in matches]
    print(set(objs))

    with open("no_result_legislations.txt",'w') as f:
        f.writelines((str(x)+"\n" for x in set(objs)))

main()