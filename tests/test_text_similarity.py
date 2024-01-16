import os
import sys
module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)
from text_utils.textSimilarity import JaccardSimilarity
import pytest


@pytest.mark.parametrize("s1, s2, result",[
    ("test sentence","test", 1/2),
    (None,"another sentence.", 0),
    (None,None,0),
    ("Some sentence.","Should not match",0),
    ("One Third match", "One Third", 2/3),
    (""," ",0),
    ("","should not match",0)
])
def test_JaccardSimilarity(s1,s2,result):
    assert JaccardSimilarity.calculate_similarity(s1,s2) == result