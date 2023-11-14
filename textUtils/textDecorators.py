from abc import ABC,abstractmethod
import re
import string
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
    if result:
        return int(result[0])
    else:
        return -1

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
        return TopDecorator
