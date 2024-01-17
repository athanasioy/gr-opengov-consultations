from typing import Protocol
import difflib

class TexteDiffAlgorithm(Protocol):
    def calculate_differences(self,txt1:str,txt2:str) -> int:
        """Calculate the number of differences between two strings"""

class TextSimilarityAlgorithm(Protocol):
    method_name:str
    def calculate_similarity(self,txt1:str,txt2:str) -> float:
        """calculate the similarity between two texts"""


class LineDifferenceAlgorithm:
    def __init__(self):
        self._seqMatcher = difflib.SequenceMatcher()


    def calculate_differences(self,s1:str,s2:str) -> int:
        s1_l = s1.split(" ") if s1 is not None else ""
        s2_l = s2.split(" ") if s2 is not None else ""
        diffs = difflib.ndiff(s1_l,s2_l)
        count = sum((1 for i in diffs if i[0]=='+' or i[0]=='-'))
        return count

    def show_diffs(self,s1:str,s2:str) -> list[str]:
        s1_l = s1.split(" ") if s1 is not None else ""
        s2_l = s2.split(" ") if s2 is not None else ""
        deltas = list(difflib.ndiff(s1_l,s2_l))
        return deltas

    def calculate_similarity(self,s1:str,s2:str) -> float:
        """formula=2.0*M / T
        where:
            M is the number of matches
            T is the total number of elements
        """ 
        s1 = s1 or ""
        s2 = s2 or ""
        self._seqMatcher.set_seqs(s1,s2)

        return self._seqMatcher.ratio()
        