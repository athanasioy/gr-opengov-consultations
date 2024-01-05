import os
import sys
module_path = os.path.abspath(os.path.join('.'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

from data_objects.article import Article
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import text
from sqlalchemy import create_engine, select, Integer
from configparser import ConfigParser

from text_utils.textEmbeddings import GreekBERTEncoder

MAX_TOKEN_SIZE = 512
def main():
    config = ConfigParser()
    config.read('config.ini')
    engine = create_engine(config.get('DEFAULT','db_file'))
    
    encoder = GreekBERTEncoder()
    
    AnalysisArticles = text("""SELECT p_ArticleId from ArticleAnalysis
                            UNION SELECT f_ArticleID from ArticleAnalysis""")\
                            .columns(p_ArticleId=Integer)
    
    stmt = select(Article.text).where(Article.id.in_(AnalysisArticles))
    
    
    text_all = 0
    text_above_512 = 0
    with Session(engine) as sess:
        rows = sess.execute(stmt).scalars()
        for row in rows:
            token = encoder._tokenizer(row, return_tensors="pt")
            token_size = token['input_ids'].size(1)
            
            if token_size>MAX_TOKEN_SIZE:
                text_above_512 +=1
            text_all +=1
    
    print(f"Number of Text above {MAX_TOKEN_SIZE} token {text_above_512} of {text_all} ({text_above_512/text_all:.2f})")
main()