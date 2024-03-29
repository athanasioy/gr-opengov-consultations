import os
import sys

module_path = os.path.abspath(os.path.join("."))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

from sqlalchemy.sql import text
from sqlalchemy import create_engine
from typing import Any
import configparser
import argparse
from text_utils.textAlgorithms import (
    LineDifferenceAlgorithm,
    TexteDiffAlgorithm,
    TextSimilarityAlgorithm,
)
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()

parser.add_argument(
    "mapping_version", help="possible values are v1 (ArticleMappings) and v2 (Article)"
)

args = parser.parse_args()


def create_article_analysis_dictionary(
    sqlRow,
    DifferenceAlgorithm: TexteDiffAlgorithm,
    SimilarityAlgorith: TextSimilarityAlgorithm,
) -> dict[str, Any]:
    strptime_format = r"%Y-%m-%d"
    insert_params = {}
    p_articleID = sqlRow[0]
    f_articleID = sqlRow[6]
    p_legislation_id = sqlRow[1]
    p_date_str = sqlRow[4]
    f_date_str = sqlRow[9]
    if p_date_str and f_date_str:
        time_delta: timedelta = datetime.strptime(
            f_date_str, strptime_format
        ) - datetime.strptime(p_date_str, strptime_format)
        days_diff = time_delta.days
    else:
        days_diff = None
    total_comments = sqlRow[11] or 0
    comments_allowed = sqlRow[10]
    p_text = sqlRow[3]
    f_text = sqlRow[8]
    diff_count = DifferenceAlgorithm.calculate_differences(p_text, f_text)
    similarity_ratio = SimilarityAlgorith.calculate_similarity(p_text, f_text)
    p_articleNo = sqlRow[2]
    f_articleNo = sqlRow[5]

    insert_params["p_articleID"] = p_articleID
    insert_params["f_articleID"] = f_articleID
    insert_params["p_legislation_id"] = p_legislation_id
    insert_params["days_diff"] = days_diff
    insert_params["total_comments"] = total_comments
    insert_params["diff_count"] = diff_count
    insert_params["similarity_ratio"] = similarity_ratio
    insert_params["comments_allowed"] = comments_allowed
    insert_params["p_articleNo"] = p_articleNo
    insert_params["f_articleNo"] = f_articleNo

    return insert_params


def main():
    use_v1 = False
    use_v2 = False
    mapping_version = args.mapping_version
    match mapping_version:
        case "v1":
            use_v1 = True
        case "v2":
            use_v2 = True
        case _:
            print("Allowed values for mapping_version argument are either v1 or v2")
            raise SystemExit(1)
    diffAlgorithm = LineDifferenceAlgorithm()
    config = configparser.ConfigParser()
    config.read("config.ini")
    engine = create_engine(config.get("DEFAULT", "db_file"))

    # delete Article Analysis Table before recreation
    with engine.connect() as conn:
        deleteStmt = "DELETE FROM ArticleAnalysis"
        conn.execute(text(deleteStmt))
        conn.commit()

    if use_v1:
        sqlText = """SELECT 	Article.id,
                            Article.legislation_id,
                            Article.Number,
                            Article.text,
                            Legislation.date_posted as p_legislation_date_posted,
                            A.joinNum,
                            FinalArticles.id as final_article_id,
                            FinalArticles.legislation_id as final_legislation_id,
                            FinalArticles.Text as FinalText,
                            FinalLegislation.date_posted as f_legislation_date_posted,
                            Article.comments_allowed,
                            comments_count.total_comments
                    FROM Article
                    INNER JOIN Legislation on Legislation.id = Article.legislation_id and Legislation.final_legislation_id is not NULL
                    LEFT JOIN Legislation as FinalLegislation on FinalLegislation.id = Legislation.final_legislation_id
                    LEFT JOIN (

                    SELECT 	A.legislation_id,
                            A.Number,
                            ArticleMapping.final_legislation_article_no,
                            coalesce(row_number() OVER (PARTITION by A.legislation_id,A.MaxMappedArticle order by CAST(A.number AS INT)) -1 + ArticleMapping.final_legislation_article_no, cast(A.number as int)) as joinNum
                    FROM (
                        SELECT 	Article.legislation_id,
                                Article.number,
                                MAX(ArticleMapping.public_consultation_article_no) OVER (PARTITION BY Article.legislation_id,Article.number) as MaxMappedArticle
                        FROM Article
                        LEFT JOIN Legislation on Legislation.id = Article.legislation_id
                        LEFT JOIN ArticleMapping on ArticleMapping.legislation_id = Article.legislation_id
                                    and Article.number >= ArticleMapping.public_consultation_article_no
                        WHERE Legislation.is_public_consultation=1
                    ) AS A
                    LEFT JOIN 	ArticleMapping on ArticleMapping.legislation_id = A.legislation_id
                                AND ArticleMapping.public_consultation_article_no = A.MaxMappedArticle
                    GROUP BY A.legislation_id, A.number, A.MaxMappedArticle,ArticleMapping.final_legislation_article_no

                    )
                    AS A
                    ON A.legislation_id = Article.legislation_id and A.number = Article.number
                    LEFT JOIN Article as FinalArticles on FinalArticles.legislation_id = Legislation.final_legislation_id AND FinalArticles.number = A.JoinNum
                    LEFT JOIN (
                        SELECT PublicConsultation .article_id, count(*) as total_comments from PublicConsultation 
                        group by PublicConsultation .article_id
                    ) as comments_count on comments_count.article_id = Article.id
                    """
    elif use_v2:
        sqlText = """
            SELECT 	Article.id,
                    Article.legislation_id,
                    Article.number,
                    Article.text,
                    Legislation.date_posted,
                    FinalArticles.number as joinNum,
                    FinalArticles.id as final_article_id,
                    FinalArticles.legislation_id as final_legislation_id,
                    FinalArticles.Text as FinalText,
                    FinalLegislation.date_posted as f_legislation_date_posted,
                    Article.comments_allowed,
                    COALESCE(comments_count.total_comments,0) as total_comments
            FROM Article
            INNER JOIN Legislation on Legislation.id = Article.legislation_id and Legislation.final_legislation_id is not NULL
            LEFT JOIN Legislation as FinalLegislation on FinalLegislation.id = Legislation.final_legislation_id
            LEFT JOIN Article as FinalArticles on FinalArticles.id = Article.voted_article_id
            LEFT JOIN (
                SELECT Article.id, count(*) as total_comments
                FROM Article
                INNER JOIN PublicConsultation on PublicConsultation.article_id = Article.id
                GROUP by Article.id
            ) as comments_count on comments_count.id = Article.id
            where Article.number <> 999
            """


    insertText = """INSERT INTO ArticleAnalysis (p_articleID,f_articleID,p_legislation_id,days_diff,diff_count,similarity_ratio,total_comments,comments_allowed,p_articleNo,f_articleNo)
                    VALUES (:p_articleID,:f_articleID,:p_legislation_id,:days_diff,:diff_count,:similarity_ratio,:total_comments,:comments_allowed,:p_articleNo,:f_articleNo)"""
    with engine.connect() as con:
        rows = con.execute(text(sqlText))

        for idx, sqlRow in enumerate(rows):
            # pprint(sqlRow[9])
            insert_params = create_article_analysis_dictionary(
                sqlRow, diffAlgorithm, diffAlgorithm
            )
            con.execute(text(insertText), insert_params)
            if idx % 500 == 0:
                print(idx, datetime.now())
            # break
        con.commit()


main()
