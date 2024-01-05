import sqlite3
import pandas as pd
def main():
    conn = sqlite3.connect("db_file.db")
    sqlText= """select articleId, Article.text from (
                            select p_articleID as articleId from ArticleAnalysis
                            UNION
                            select f_articleID as articleId from ArticleAnalysis
                    ) as a 
                    left join Article on Article.id = a.articleId"""
    df = pd.read_sql_query(sqlText,conn)
    print(df.head())
    df.to_csv("article_id_text.csv", sep=';', index=False)
main()