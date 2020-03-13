
from .normal import normalChecker
from .spj import spjChecker

from lib.static import RESULT
from lib.logger import getLogger
LOGGER = getLogger(__name__)


def checkAnswer(pid, case, is_spj, basepath, threadid):
    LOGGER.debug(threadid, str(pid) + str(case) + str(is_spj))
    if is_spj == True:
        return spjChecker(pid, case, basepath, threadid)
    else:
        return normalChecker(pid, case, basepath, threadid)
