import os
from pathlib import Path
import sys

from tqdm import tqdm

module_path = os.path.abspath(os.path.join("."))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)
from configparser import ConfigParser
import argparse
from sqlalchemy import create_engine, select, cast, Integer, func
from sqlalchemy.orm import Session, aliased
from text_utils.textAlgorithms import LineDifferenceAlgorithm, TextSimilarityAlgorithm
from data_objects.article import Article
from data_objects.legislation import Legislation

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--row_limit",
                    type=int,action="store",default=35,
                    help="Defines the range of plus-minus search of an article match. If 0, no limit")
parser.add_argument("-f","--file",
                    help="if given a file, mappings will be generated only for the selected consultations")

args = parser.parse_args()
def generate_cross_similarities(
    article: Article,
    candidate_articles: list[Article],
    similarity_algo: TextSimilarityAlgorithm,
) -> dict[int, float]:
    similarity_dict = {}
    for candidate_article in candidate_articles:
        similarity = similarity_algo.calculate_similarity(
            article.text, candidate_article.text
        )
        similarity_dict.update({int(candidate_article.id): similarity})
    return similarity_dict


def main():
    config = ConfigParser()
    config.read("config.ini")
    sqlalchemy_conn_string = config.get(section="DEFAULT", option="db_file")
    engine = create_engine(sqlalchemy_conn_string)

    ROW_LIMIT = args.row_limit
    if ROW_LIMIT ==0:
        ROW_LIMIT =999

    legislation_file_path = args.file
    if legislation_file_path:
        legislation_file_path_obj = Path(legislation_file_path)
        if legislation_file_path_obj.is_dir():
            print(f"File path {legislation_file_path_obj} must a file, not a directory")
            raise SystemExit(1)
        if not legislation_file_path_obj.exists():
            print(f"file path {legislation_file_path} does not exist.")
            raise SystemExit(1)
        legislations_to_consider = legislation_file_path_obj.read_text(encoding='utf8').split()
        if not isinstance(legislations_to_consider,list):
            print("File must contain only public consultation id seperated by new line")
            raise SystemExit(1)

    voted_articles_aliased = aliased(Article, name="voted_articles")
    similarity_algo = LineDifferenceAlgorithm()
    with Session(engine) as sess:

        if legislations_to_consider:  # If file is passed, consider only legislations in file
            proposed_articles_stmt = (
                select(Article)
                .join(Legislation.articles)
                .where(~Legislation.final_legislation_id.is_(None),
                       Legislation.id.in_(legislations_to_consider))
            )
        else:
            proposed_articles_stmt = (
                select(Article)
                .join(Legislation.articles)
                .where(~Legislation.final_legislation_id.is_(None))
            )

        if legislations_to_consider:
            proposed_articles_stmt_cnt = (
                select(func.count()).select_from(Article)
                .join(Legislation.articles)
                .where(~Legislation.final_legislation_id.is_(None),
                       Legislation.id.in_(legislations_to_consider))
            )
        else:
            proposed_articles_stmt_cnt = (
                select(func.count()).select_from(Article)
                .join(Legislation.articles)
                .where(~Legislation.final_legislation_id.is_(None))
            )
        # Get Matched Public Consultation Articles
        rows = sess.execute(proposed_articles_stmt).scalars()
        cnt = sess.execute(proposed_articles_stmt_cnt).scalar()
        print(f"Total Articles : {cnt}")
        print(f"Row Limit: {ROW_LIMIT}")
        for idx, article in enumerate(rows):
            # for each article, try to find best matching article within ROW_LIMIT range
            voted_articles_stmt = (
                select(voted_articles_aliased)
                .join(Legislation.articles)
                .join(
                    voted_articles_aliased,
                    voted_articles_aliased.legislation_id
                    == Legislation.final_legislation_id,
                )
                .where(
                    Article.id == article.id,
                    cast(Article.number, Integer) >= cast(voted_articles_aliased.number, Integer) - ROW_LIMIT,
                    cast(Article.number, Integer) <= cast(voted_articles_aliased.number, Integer) + ROW_LIMIT,
                )
            )
            voted_articles = sess.execute(voted_articles_stmt).scalars().all()
            if not voted_articles:
                continue
            similarities = generate_cross_similarities(
                article, voted_articles, similarity_algo
            )
            most_similar_id = max(similarities, key=lambda x: similarities.get(x))
            most_similar_article = list(
                filter(lambda x: x.id == most_similar_id, voted_articles)
            )[0]
            print(
                f"{article.number}, {article.id}, {similarities.get(most_similar_id)}, {most_similar_article.number}"
            )
            article.voted_article = most_similar_article
            if ( idx ) % 1000 == 0:
                print(f"Progress: {idx/cnt:.2f}")
                sess.commit()


main()
