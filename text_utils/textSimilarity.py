from typing import Protocol
import numpy as np

class Vectorizer(Protocol):
    def vectorize(self,s1:str) -> np.ndarray:
        """Produce a vector representation of String"""


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

        return np.dot(v1,v2)/(np.linalg.norm(v1)* np.linalg.norm(v2))

