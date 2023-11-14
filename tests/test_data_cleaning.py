import sys
import os
# C:\Users\aneme\vscode\publicConsulationScrap
module_path = os.path.abspath(os.path.join('.'))
print(module_path)
# add public consultation folder to import search paths
if module_path not in sys.path:
    sys.path.append(module_path)

from textUtils.textDecorators import RemoveNewLineDecorator, RemoveDashAndNewLineDecorator,TextDecoratorChainFactory, TrimWhiteSpaceDecorator, ReplaceWrongGreekMuCharacterDecorator


def test_newLine_removal() -> None:
    txt = """νέα\nγραμμή"""
    newLineRemoval = RemoveNewLineDecorator(None)
    assert(newLineRemoval.execute(txt) == "νέα γραμμή")

def test_dashAndNewLine_removal() ->None:
    txt = """νέα γραμ-\nμή με παύλα"""
    dashRemovalDecorator = RemoveDashAndNewLineDecorator(None)
    
    assert(dashRemovalDecorator.execute(txt)=="νέα γραμμή με παύλα")

def test_whiteSpace_removal()->None:
    txt ="   νέα γραμμή   "
    whitespaceRemovalDecorator = TrimWhiteSpaceDecorator(None)
    assert (whitespaceRemovalDecorator.execute(txt)=="νέα γραμμή")

def test_newLineAndRemoveDashDecorator_chain() -> None:
    txt = "νέα γραμ-\nμή με παύλα\nκαι νέα γραμμή"
    decoratorChain = RemoveNewLineDecorator(None)
    decoratorChain = RemoveDashAndNewLineDecorator(decoratorChain)

    assert (decoratorChain.execute(txt) == "νέα γραμμή με παύλα και νέα γραμμή")

def test_chain_decorator() -> None:
    txt ="""
1. Εάν η Εθνική Αρχή Κυβερνοασφάλειας, αφότου διε-
ξαγάγει αξιολόγηση ή έλεγχο σύµφωνα µε το άρθρο 36,
"""
    decoratorChain = TextDecoratorChainFactory.createDecoratorChain(applyLower=True)
    assert(decoratorChain.execute(txt)=="1. εάν η Εθνική Αρχή Κυβερνοασφάλειας, αφότου διεξαγάγει αξιολόγηση ή έλεγχο σύµφωνα µε το άρθρο 36,".lower())
           
def test_greek_mu_decorator()->None:
    s1 = "νομίμου" # correct
    s2 = "νοµίµου" # incorrect
    assert s1 != s2
    decorator = ReplaceWrongGreekMuCharacterDecorator(None)
    s2 = decorator.execute(s2)
    assert s1 == s2
