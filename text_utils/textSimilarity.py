from typing import Protocol
import numpy as np
from sqlalchemy import create_engine, text
from text_utils.helpers import db_to_numpy

class Vectorizer(Protocol):
    def vectorize(self,s1:str) -> np.ndarray:
        """Produce a vector representation of String"""

class FetchFromDBVectorizer:
    def __init__(self,conn_string:str,table_name:str) -> None:
        self._conn_string = conn_string
        self._engine = create_engine(self._conn_string)
        self._embeddings:dict[str,np.ndarray] = {}
        self._populate_embeddings(table_name)

    def _populate_embeddings(self,table_name) -> None:
        sql_text = f"""
        select articleId, Article.text from (
                            select p_articleID as articleId from {table_name}
                            UNION
                            select f_articleID as articleId from {table_name}
                    ) as a 
                    left join Article on Article.id = a.articleId
        """
        with self._engine.connect() as conn:
            rows = conn.execute(text(sql_text))
            for row in rows:
                article_id = row[0]
                article_text = row[1]
                vector = db_to_numpy(conn, article_id)
                self._embeddings.update({article_text:vector})

                
    def vectorize(self, s:str) -> np.ndarray:
        return self._embeddings[s]
class JaccardSimilarity:
    method_name='Jaccard'
    @staticmethod
    def calculate_similarity(s1:str,s2:str) -> float:
        if not s1 or not s2:  # if either string is null or empty
            return 0.0

        s1 = s1.split(' ')
        s2 = s2.split(' ')
        return len(set.intersection(set(s1),set(s2))) / len(set.union(set(s1),set(s2)))

class CosineSimilarity:
    method_name='Cosine'

    def __init__(self, vectorizer:Vectorizer) -> None:
        self._vectorizer = vectorizer


    def calculate_similarity(self,s1:str,s2:str) -> float:
        v1 = self._vectorizer.vectorize(s1)
        v2 = self._vectorizer.vectorize(s2)
        length_v1 = np.linalg.norm(v1)
        length_v2 = np.linalg.norm(v2)

        if length_v1==0 or length_v2==0:
            return 0.0
        return np.dot(v1,v2)/(np.linalg.norm(v1)* np.linalg.norm(v2))

