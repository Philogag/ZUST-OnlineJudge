
from .normal import normalChecker
from .spj import spjChecker

from lib.static import RESULT

def checkAnswer(pid, case, is_spj):
    if is_spj == True:
        return spjChecker(pid, case)
    

    else:
        return normalChecker(pid, case)