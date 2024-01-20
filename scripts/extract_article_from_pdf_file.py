import os
import sys
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
import argparse
from collections import defaultdict
import re
from glob import glob
from pprint import pprint
from configparser import ConfigParser
from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from text_utils.helpers import text_to_numeric
from data_objects.legislation import Legislation
from data_objects.article import Article
from text_utils.textDecorators import TextDecoratorChainFactory

parser = argparse.ArgumentParser()

parser.add_argument("bill_id")
parser.add_argument("-ft", "--full_text", action="store_true", default=False)
parser.add_argument("-t","--test_mode",action="store_true", default=False)


args = parser.parse_args()

def main():
    bill_id = args.bill_id
    full_text_flag = args.full_text
    test_mode = args.test_mode
    end_of_bill1 = "Ο ΠΡΟΕΔΡΟ"  # Ο ΠΡΟΕΔΡΟΣ ΤΗΣ ΒΟΥΛΗΣ
    end_of_bill2 = "ΠΑΡΑΡ"  # ΠΑΡΑΡΤΗΜΑ
    txt_articles_file = glob(f"pdf_files/text/{bill_id}_articles.txt")
    txt_full_file = glob(f"pdf_files/text/{bill_id}_full.txt")

    text_decorator = TextDecoratorChainFactory.createDecoratorChain(False)

    config = ConfigParser()
    config.read('config.ini')
    sqlalchemy_conn_string = config.get(section='DEFAULT', option='db_file')
    engine = create_engine(sqlalchemy_conn_string)
    
    if len(txt_articles_file)>1:
        print(f"Multiple Articles Files Found for id {bill_id}")
        raise SystemExit(1)

    if len(txt_full_file)>1:
        print(f"Multiple full text Files Found for id {bill_id}")
        raise SystemExit(1)
    
    if len(txt_articles_file)==0:
        print(f"Zero Articles Files Found for id {bill_id}")
        raise SystemExit(1)

    if len(txt_full_file)==0:
        print(f"Zero full text Files Found for id {bill_id}")
        raise SystemExit(1)
    
    txt_articles_file = txt_articles_file[0]
    txt_full_file = txt_full_file[0]
    
    txt_articles = Path(txt_articles_file).read_text(encoding="utf-8")
    txt_articles += "ρθρ"  # Necessary in order to match last article due to regex changes on the positive lookahead (?=Ά) = (?=Άρθρ)
    txt_full = Path(txt_full_file).read_text(encoding="utf-8")

    if full_text_flag:
        articles_regex = (
            r"^[ΆΑA]ρθρ[οo]\s?([\w\s]*?)\n(.*?)(:?(?=[ΆΑA]ρθρ)|(?=ΚΕΦΑ)|(?=ΜΕΡΟΣ))"
        )
    else:
        articles_regex = r"^[ΆΑA]ρθρ[οo]\s?(\d+)(.*?)(:?(?=[ΆΑA]ρθρ)|(?=ΚΕΦΑ)|(?=ΜΕΡΟΣ))"  # id=892 Άρθρο 95 has a Latin "o"

    articles_dict = {}

    if full_text_flag:
        txt_to_numeric = {}
        matches_full_text = re.findall(
            articles_regex, txt_articles, re.DOTALL | re.MULTILINE
        )
        for m in matches_full_text:
            article_num_integer = text_to_numeric(m[0])
            original_text = m[0]
            article_title = m[1]
            if article_num_integer == -1:
                raise ValueError(
                    f"Text To Numeric Failed for PDF={txt_articles_file}, txt={m[0]}"
                )
            txt_to_numeric[original_text] = article_num_integer
            articles_dict[original_text] = article_title
    else:
        # Create Article Dict
        matches_articles = re.findall(
            articles_regex, txt_articles, re.DOTALL | re.MULTILINE
        )
        for match in matches_articles:
            articles_dict[match[0]] = match[1]

    data = defaultdict(dict)
    if full_text_flag:
        try:
            max_article_num = max((int(x) for x in txt_to_numeric.values()))
            min_article_num = min((int(x) for x in txt_to_numeric.values()))
        except ValueError as e:
            print(f"File={txt_articles_file} - Empty Sequence. Msg={str(e)} ")
            raise SystemExit(1) from e
    else:
        try:
            max_article_num = max((int(x) for x in articles_dict))
            min_article_num = min((int(x) for x in articles_dict))
        except ValueError as e:
            print(f"File={txt_articles_file} - Empty Sequence. Msg={str(e)} ")
            raise SystemExit(1) from e

    if full_text_flag:
        sorted_articles = sorted((int(x) for x in txt_to_numeric.values()))
    else:
        sorted_articles = sorted((int(x) for x in articles_dict))

    if sorted_articles != list(range(min_article_num, max_article_num + 1)):
        raise ValueError(
            f"Missing Article Numbers {set(range(min_article_num,max_article_num+1)).difference(set(sorted((int(x) for x in articles_dict.keys()))))}"
        )

    if full_text_flag:
        articles_array = list(
            sorted(articles_dict.keys(), key=text_to_numeric))
        
        max_article_num = articles_array[len(articles_array) - 1]
    else:
        articles_array = list(sorted(articles_dict.keys(), key=int))
        articles_array = list((int(x) for x in articles_array))

    for idx, k in enumerate(articles_array):
        current_article_num = k
        if idx < len(articles_array) - 1:
            next_article_num = articles_array[idx + 1]

        if current_article_num==44:
            print()
        # Try to match by Article No. And Title
        article_text_start = f"Άρθρο {current_article_num}{articles_dict[str(current_article_num)][:-1]}".strip()
        matches = list(re.finditer(article_text_start,txt_full))
        if matches:
            article_text_start_idx = matches[len(matches)-1].start()
            flag_use_full_title_in_search = True
        else:
            article_text_start_idx =-1

        if article_text_start_idx == -1:
            # if matching  by title fails, match by article
            flag_use_full_title_in_search = False
            m = re.search(
                r"[ΆΑA]ρθρ[οo]\s?" + str(current_article_num) + "\n", txt_full
            )
            if m is not None:
                article_text_start_idx = m.start()

        if article_text_start_idx == -1:
            raise ValueError(
                f"File={txt_articles_file}Cannot find text {article_text_start} in full_text"
            )

        if current_article_num != max_article_num:
            # article_text_end = f"Άρθρο {next_article_num}{articles_dict[str(next_article_num)]}".strip()
            article_text_end = f"Άρθρο {next_article_num}{articles_dict[str(next_article_num)][:-1]}".strip()
            matches = list(re.finditer(article_text_end,txt_full))
            if matches:
                article_text_end_idx = matches[len(matches)-1].start()
                flag_use_full_title_in_search = True
            else:
                article_text_end_idx=-1
                # article_text_end_idx = txt_full.find(article_text_end)

            if article_text_end_idx == -1:
                # if None, try to match only the article number
                m = re.search(
                    r"[ΆΑA]ρθρ[οo]\s?" + str(next_article_num) + "\n", txt_full
                )
                if m is not None:
                    article_text_end_idx = m.start()
                    article_text_end = m.group()

            if article_text_end_idx == -1:
                raise ValueError(
                    f"File={txt_articles_file} Cannot find text {article_text_end} in full_text"
                )

        else:
            if txt_full.rfind(end_of_bill2) > 0:
                article_text_end_idx = txt_full.rfind(end_of_bill2)  # ΠΑΡΑΡΤΗΜΑ
            elif txt_full.rfind(end_of_bill1) > 0:
                article_text_end_idx = txt_full.rfind(end_of_bill1)  # Ο ΠΡΟΕΔΡΟΣ
            else:
                article_text_end_idx = len(txt_full)

        article_text = txt_full[
            article_text_start_idx + len(article_text_start) : article_text_end_idx
        ]

        if (
            not flag_use_full_title_in_search
        ):  # if seach did not use full article title, try to remove on this step
            article_text = article_text.replace(
                articles_dict[str(current_article_num)], "", 1
            )  # remove title from text

        data[k].update({"title": articles_dict[str(current_article_num)]})
        data[k].update({"text": article_text})

    # pprint(data[44])
    with Session(engine) as sess:
        legislation_id = re.search(r"\d+",txt_articles_file)[0]
        stmt = select(Legislation).where(Legislation.id==legislation_id)
        legObj = sess.execute(stmt).scalar_one()

        for article,text_and_title in data.items():
            article_num: int
            if full_text_flag:
                article_num = text_to_numeric(article)
            else:
                article_num = article

            articleObj:Article
            if article_num not in (int(legiglationArticlesObj.number) for legiglationArticlesObj in legObj.articles):
                articleObj = Article(number=article_num,title=text_and_title['title'], text=text_and_title['text'])
                legObj.articles.append(articleObj)
            else:
                articleObj = next(filter(lambda x : int(x.number)==article_num, legObj.articles))
                articleObj.text = text_decorator.execute(text_and_title['text'])
                articleObj.title = text_decorator.execute(text_and_title['title'])

                
        if not test_mode:
            sess.commit()

main()