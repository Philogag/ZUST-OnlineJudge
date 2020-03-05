import os
import difflib

# from ..tool.logging import getLogger
# LOGGER = getLogger(__name__)

OK = 0
PE = 1
WA = 2
SE = 4

def compareMain(filea, fileb):
    ret = os.system("diff -qNZa " + filea + " " + fileb + " >/dev/null 2>&1") # 忽略所有行末空格
    if ret != 0:
        ret = 1
        ret += os.system("diff -qNa -iEwB " + filea + " " + fileb + " >/dev/null 2>&1")  # 忽略所有空格空行和大小写
        if ret != 1:
            ret = 2
    # LOGGER.debug(str(ret))
    return ret

if __name__ == "__main__":
    print(compareMain("./temp/userout.txt", "./ProblemData/1/1.out"))