from abc import ABC,abstractmethod
import re
import string
class Component(ABC):
    @abstractmethod
    def execute(self,s:str) -> str:
        pass

class StrLower(Component):
    def execute(self, s: str) -> str:
        return str.lower(s)

class Decorator(Component):
    def __init__(self,component:Component):
        self._decorated = component


class TrimWhiteSpaceDecorator(Decorator):
    def execute(self,text:str):
        s = text.strip()
        if self._decorated is not None:
            s = self._decorated.execute(s)
        return s

class RemoveNewLineDecorator(Decorator):
    def execute(self, s: str) -> str:
        PATTERN = r"(.)\n"
        s = re.sub(PATTERN,r"\1 ",s)
        if self._decorated is not None:
            s = self._decorated.execute(s)
        return s

class RemoveDashAndNewLineDecorator(Decorator):
    def execute(self, s: str) -> str:
        PATTERN = r"(\w)-\n"
        s = re.sub(PATTERN,r"\1",s)
        if self._decorated is not None:
            s = self._decorated.execute(s)
        return s


class RemovePunctuationDecorator(Decorator):
    def execute(self, s: str) -> str:
        transtable = str.maketrans('','',string.punctuation)
        s = s.translate(transtable)
        if self._decorated is not None:
            s = self._decorated.execute(s)
        return s

class ReplaceWrongGreekMuCharacterDecorator(Decorator):
    def execute(self, s: str) -> str:
        wrong_greek_mu = bytes.decode(b"\xc2\xb5", encoding='utf-8')
        correct_greek_mu = bytes.decode(b"\xce\xbc", encoding='utf-8')
        s = s.replace(wrong_greek_mu,correct_greek_mu)
        if self._decorated is not None:
            s = self._decorated.execute(s)
        return s

        
class TextDecoratorChainFactory():
    @staticmethod
    def createDecoratorChain(applyLower:bool) -> Decorator:
        """Decorators are applied in a Last-In First-Out fashion.
        I.E:
        TopDecorator = RemoveDashAndNewLineDecorator(None)
        TopDecorator = TrimWhiteSpaceDecorator(TopDecorator)
        Execution:
        TrimWhiteSpaceDecorator -> RemoveDashAndNewLineDecorator
        """
        if applyLower:
            TopDecorator = RemoveNewLineDecorator(StrLower())
        else:
            TopDecorator = RemoveNewLineDecorator(None)
        
        TopDecorator = RemoveDashAndNewLineDecorator(TopDecorator)
        TopDecorator = TrimWhiteSpaceDecorator(TopDecorator)
        TopDecorator = ReplaceWrongGreekMuCharacterDecorator(TopDecorator)
        return TopDecorator
