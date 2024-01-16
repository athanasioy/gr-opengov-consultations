
class JaccardSimilarity:
    
    @staticmethod
    def calculate_similarity(s1:str,s2:str) -> float:
        if not s1 or not s2:  # if either string is null or empty
            return 0.0

        s1 = s1.split(' ')
        s2 = s2.split(' ')
        
        return len(set.intersection(set(s1),set(s2))) / len(set.union(set(s1),set(s2)))
