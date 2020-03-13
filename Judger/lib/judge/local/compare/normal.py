import os
import difflib

from lib.logger import getLogger
from lib.config import GlobalConf
from lib.static import RESULT
LOGGER = getLogger(__name__)

def normalChecker(pid, case, basepath, threadid) -> (int, str):
    filea = os.path.join(basepath, 'userout.txt')
    fileb = os.path.join(GlobalConf["path"], 'ProblemData/%d/%s.out' % (pid, case))
    
    ret = os.system("diff -qNZa " + filea + " " + fileb + " >/dev/null 2>&1") # 忽略所有行末空格
    if ret != 0:
        ret = os.system("diff -qNa -iEwB " + filea + " " + fileb + " >/dev/null 2>&1")  # 忽略所有空格空行和大小写
        if ret != 0:
            return RESULT.WRONG_ANSWER
        else:
            return RESULT.FORMAT_ERROR
    else:
        return RESULT.ACCEPT

if __name__ == "__main__":
    print(normalChecker("./temp/userout.txt", "./ProblemData/1/1.out"))