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
    
def db_to_numpy(conn, article_id:int) -> np.ndarray:
    selectSql = """SELECT vector FROM ArticleEmbeddings WHERE articleId = :articleId"""
    selectParams = {}
    selectParams["articleId"] = article_id
    try:
        vector_blob = conn.execute(text(selectSql),selectParams).scalar_one()
        vector = np.frombuffer(vector_blob,dtype=float)
    except:
        print(f'Failed to find embeddings for id {article_id}')
        raise
        
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
    return int(result[0]) if result else -1
