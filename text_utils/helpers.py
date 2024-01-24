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
    
def db_to_numpy(conn, article_id:int) -> np.ndarray:
    selectSql = """SELECT vector FROM ArticleEmbeddings WHERE articleId = :articleId"""
    selectParams = {}
    selectParams["articleId"] = article_id
    vector_blob = conn.execute(text(selectSql),selectParams).scalar_one()
    vector = np.frombuffer(vector_blob,dtype=float)
        
    return vector

def text_to_numeric(text:str) -> int:
    numbers_in_full_text:list[tuple[str,int]] = [
        ("πρώτο",1),
        ("δεύτερο",2),
        ("τρίτο",3),
        ("τέταρτο",4),
        ("πέμπτο",5),  # greek μ encoded as "ce bc" in utf-8
        ("πέµπτο",5),  # MICRO SIGN "µ" encoded as "c2 b5" in utf-8 PRESENT IN 1247_articles
        ("έκτο",6),
        ("έβδομο",7),  # greek μ encoded as ce bc in utf-8
        ("έβδοµο",7),   # MICRO SIGN "µ" encoded as c2 b5 in utf-8 PRESENT IN 1247_articles
        ("όγδοο",8),
        ("ένατο",9),
        ("δέκατο",10),
        ("δέκα",10),
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
