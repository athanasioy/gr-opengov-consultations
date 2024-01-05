import sys
import os
from  pathlib import Path
from pprint import pprint
from text_utils.textDecorators import ReplaceWrongGreekMuCharacterDecorator, RemovePunctuationDecorator
# C:\Users\aneme\vscode\publicConsulationScrap
module_path = os.path.abspath(os.path.join('.'))
print(module_path)
# add public consultation folder to import search paths
if module_path not in sys.path:
    sys.path.append(module_path)

from text_utils.textAlgorithms import LineDifferenceAlgorithm
import pytest



@pytest.mark.parametrize("file1, file2, result",[
    (
        r"tests\test_difference_files\p1.txt",
        r"tests\test_difference_files\f1.txt",
        0
     ),
     (
         r"tests\test_difference_files\p2.txt",
         r"tests\test_difference_files\f2.txt",
         2
     ),
     (
        r"tests\test_difference_files\p3.txt",
        r"tests\test_difference_files\f3.txt",
        2
     )
])
def test_LineDifference_result(file1,file2,result) -> None:
    # Change in Words are accounted as 2 changes
    # Additions or substractions are accounted for as 1 change
    # Words are splitted by whitespace (" ")
    p1 = Path(file1).read_text(encoding='utf-8')
    f1 = Path(file2).read_text(encoding='utf-8')
    dec = ReplaceWrongGreekMuCharacterDecorator(None)
    # dec = RemovePunctuationDecorator(dec)
    p1 = dec.execute(p1)
    f1 = dec.execute(f1)
    algo = LineDifferenceAlgorithm()
    diff_count = algo.calculate_differences(p1,f1)
    pprint(algo.show_diffs(p1,f1))
    assert diff_count == result