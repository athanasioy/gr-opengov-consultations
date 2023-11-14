from typing import Protocol
import difflib

class TexteDiffAlgorithm(Protocol):
    def calculate_differences(txt1:str,txt2:str) -> int:
        """Calculate the number of differences between two strings"""
        pass

class TextSimilarityAlgorithm(Protocol):
    def calculate_similarity(txt1:str,txt2:str) -> float:
        """calculate the similarity between two texts"""
        pass


class LineDifferenceAlgorithm:
    def __init__(self):
        self._seqMatcher = difflib.SequenceMatcher()


    def calculate_differences(self,s1:str,s2:str) -> int:
        diffs = difflib.ndiff(s1.split(" "),s2.split(" "))
        count = sum((1 for i in diffs if i[0]=='+' or i[0]=='-'))
        return count

    def show_diffs(self,s1:str,s2:str) -> list[str]:
        deltas = list(difflib.ndiff(s1.split(" "),s2.split(" ")))
        return deltas

    def calculate_similarity(self,s1:str,s2:str) -> float:
        """formula=2.0*M / T
        where:
            M is the number of matches
            T is the total number of elements
        """ 
        self._seqMatcher.set_seqs(s1,s2)

        return self._seqMatcher.ratio()
        