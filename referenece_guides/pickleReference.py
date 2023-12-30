import pickle
from typing import Any

# Create a picklable Object
someObj = {}
someObj.update({'a':1})
someObj.update({'b':2})
print("My Object",someObj)
# Create a pickle file
with open(r'refereneceGuides\somePickle.bin','wb') as f:
    pickle.dump(someObj,f)


# Read a pickle file
with open(r'refereneceGuides\somePickle.bin','rb') as f:
    someObj_likeNew = pickle.load(f)


print("someObj_likeNew",someObj_likeNew)

# use __reduce__ to execute arbitrary code during unpickling

class Attack:
    def __reduce__(self) -> str | tuple[Any, ...]:
        return (eval,("print('Malicious Code')",))

malicious = pickle.dumps(Attack())  # Use dumpS to dump into bytes

pickle.loads(malicious)  # Use loadS to load bytes