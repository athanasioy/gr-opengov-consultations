import re
from pathlib import Path

def text_to_numeric(text:str) -> int:
    numbers_in_full_text:list[tuple[str,int]] = [
        ("πρώτο",1),
        ("δεύτερο",2),
        ("τρίτο",3),
        ("τέταρτο",4),
        ("πέμπτο",5),  # greek μ encoded as ce bc in utf-8
        ("πέµπτο",5),  # MICRO SIGN "µ" encoded as c2 b5 in utf-8 PRESENT IN 1247_articles
        ("έκτο",6),
        ("έβδομο",7),  # greek μ encoded as ce bc in utf-8
        ("έβδοµο",7),   # MICRO SIGN "µ" encoded as c2 b5 in utf-8 PRESENT IN 1247_articles
        ("όγδοο",8),
        ("ένατο",9),
        ("δέκατο",10),
        ("ενδέκατο",11),
        ("ένδέκατο",11),  # 1296
        ("δωδέκατο",12),
        ("δέκατο τρίτο",13),
        ("δέκατο τέταρτο",14),
        ("δέκατο πέµπτο",15),
        ("δέκατο έκτο",16),
        ("δέκατο έβδοµο",17),
        ("δέκατο όγδοο",18),
        ("δέκατο ένατο",19),
        ("εικοστό",20),
        ("εικοστό πρώτο",21),
        ("εικοστό δεύτερο",22),
        ("εικοστό τρίτο",23),
        ("εικοστό τέταρτο",24),
        ("εικοστό πέµπτο",25),
        ("εικοστό έκτο",26),
        ("εικοστό έβδοµο",27),
        ("εικοστό όγδοο",28),
        ("εικοστό ένατο",29),
        ("τριακοστό",30),
        ("τριακοστό πρώτο",31),
        ("τριακοστό δεύτερο",32)
    ]
    result = [x[1] for x in numbers_in_full_text if x[0]==text]
    if result:
        return int(result[0])
    else:
        return -1
    

def main() -> None:
    bills_with_full_text_article_numbers = set(
    ('1279',
    '1247',
    '1296',
    '1307',
    '1376',
    '1418',
    '1423')
    )

    articles_full_text_pattern = r"^[ΆΑA]ρθρ[οo]\s?([\w\s]*?)\n(.*?)(:?(?=[ΆΑA]ρθρ)|(?=ΚΕΦΑ)|(?=ΜΕΡΟΣ))"

    pdf_a = Path("pdf_files/text/1307_articles.txt")

    t=pdf_a.read_text(encoding='utf-8')

    matches = re.findall(articles_full_text_pattern, t,re.DOTALL|re.MULTILINE)

    for m in matches:
        # print(m[0] + '->' + m[1])
        if text_to_numeric(m[0])==-1:
            raise ValueError()
        print(m[0] + " ==> " +str(text_to_numeric(m[0])) + '->' + m[1])

main()
