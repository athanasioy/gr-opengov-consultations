import os
import sys
module_path = os.path.abspath(os.path.join('.'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)
    
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from text_utils.textEmbeddings import GreekBERTEncoder, GreekLongFormerEncoder
from configparser import ConfigParser
from text_utils.helpers import numpy_to_db, db_to_numpy, numpy_to_db_batch
import tqdm

MAX_TOKEN_SIZE=512
BATCH_SIZE = 16

def main():
    config = ConfigParser()
    config.read("config.ini")
    engine = create_engine(config.get('DEFAULT','db_file'))
    
    encoder = GreekLongFormerEncoder()
    
    sqlText = """select articleId, Article.text from (
                        select p_articleID as articleId from ArticleAnalysis
                        UNION
                        select f_articleID as articleId from ArticleAnalysis
                ) as a 
				left join Article on Article.id = a.articleId
                where a.articleId not in (select articleId from ArticleEmbeddings )"""
    
    with engine.connect() as conn:
        rows = conn.execute(text(sqlText))
        ids = []
        text_batch = []
        # for row in tqdm.tqdm(rows):
        for row in rows:
            _id = row[0]
            article_text = row[1]
            text_batch.append(article_text)
            ids.append(_id)
            if len(text_batch)<=BATCH_SIZE:
                continue
            else:
                vectors, token_sizes = encoder.get_embeddings_batch(input_text=text_batch)         
                numpy_to_db_batch(conn=conn,article_id=ids, vector=vectors, token_size=token_sizes)
                ids=[]
                text_batch = []
                break
        
            
main()