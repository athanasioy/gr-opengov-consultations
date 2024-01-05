import numpy as np
from sqlalchemy.sql import text
from typing import Any

def numpy_to_db(conn, article_id:int, vector:np.ndarray,token_size:int=None) ->None:
    insertSql = """INSERT INTO ArticleEmbeddings (articleId, vector,token_size) VALUES (:articleId, :vector,:token_size)"""
    insertParams = {}
    insertParams["articleId"] = article_id
    insertParams["vector"] = vector.tobytes()
    insertParams["token_size"] = token_size
    # with engine.connect() as conn:
    conn.execute(text(insertSql),insertParams)
    conn.commit()
    
def numpy_to_db_batch(conn, article_ids:list[int], vectors:list[np.ndarray], token_sizes:list[int]=None):
    assert len(article_ids)==len(vectors)
    if token_sizes is not None:
        assert len(article_ids)==len(token_sizes)
    
    insertSql = """INSERT INTO ArticleEmbeddings (articleId, vector,token_size) VALUES (:articleId, :vector,:token_size)"""
    insertParams:list[dict[str,Any]] = list()
    
    for article_id, vector, token_size in zip(article_ids,vectors,token_sizes):
        insertParams_dict = {}
        insertParams_dict["articleId"] = article_id
        insertParams_dict["vector"] = vector.tobytes()
        insertParams_dict["token_size"] = token_size
        insertParams.add(insertParams_dict)
    conn.execute(text(insertSql),insertParams)
    conn.commit()
    
def db_to_numpy(engine, article_id:int) -> np.ndarray:
    selectSql = """SELECT vector FROM ArticleEmbeddings WHERE articleId = :articleId"""
    selectParams = {}
    selectParams["articleId"] = article_id
    with engine.connect() as conn:
        rows = conn.execute(text(selectSql),selectParams)
        for row in rows:
            vector = np.frombuffer(row[0],dtype=float)
            break
        
    return vector