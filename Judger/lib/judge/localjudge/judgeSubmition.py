import json
import time
import os

from ...tool.Conf import GlobalConf
from ...tool.ToFile import toFile
from ...compile.compile import compileFile

from ...Return import Return
from .judgeCase import *

from ...tool.logging import getLogger
LOGGER = getLogger(__name__)

def getlang(lang):
    if "c++" in lang:
        return "c++"
    elif "c" in lang:
        return "c"
    elif "java" in lang:
        return "java"
    elif "python2" in lang:
        return "py2"
    elif "python3" in lang:
        return "py3"
    return None

def localJudge(submition):
    LOGGER.info("Get a submition id = " + str(submition["submitId"]))
    Return().send({"submitId": submition["submitId"], "result": RESULT.JUDGING, "msg": ""})

    # 检测语言种类
    submition["lang"] = getlang(submition["lang"])
    if submition["lang"] == None:
        LOGGER.warn("Code language type not found")
        Return().send(  # 此处返回 System Error
            {
                "submitId": submition["submitId"],
                "result": RESULT.SYSTEM_ERROR,
                "msg": "Code language type not found",
            }
        )
        return False

    # 尝试写入代码文件
    if not toFile(submition["lang"], submition["code"]):
        LOGGER.warn("Write to file faild")
        Return().send(  # 此处返回 System Error
            {
                "submitId": submition["submitId"],
                "result": RESULT.SYSTEM_ERROR,
                "msg": "Write to file faild",
            }
        )
        return False

    # 尝试编译
    comp, errcode = compileFile(submition["lang"])
    if not comp:
        LOGGER.warn("Compile faild")
        Return().send(  # 此处返回 Compile Error
            {
                "submitId": submition["submitId"],
                "result": RESULT.COMPILE_ERROR,
                "msg": "Compile faild\n" + errcode,
            }
        )
        return False

    # 检测spj并编译，TODO
    if submition["spj"] == True:
        pass

    case = []
    total_status = RESULT.ACCEPT
    for f in os.listdir("./ProblemData/%d" % submition["problemId"]):
        if f[-3:] == ".in":
            onecase = JudgeCase(
                submition["problemId"],
                f[:-3],
                submition["spj"],
                submition["time_lim"],
                submition["mem_lim"],
                submition["lang"],
            )
            case.append(onecase)
            if (
                onecase["result"] == RESULT.ACCEPT  # 无错误
                or total_status == onecase["result"]  # 同种错误
                or total_status == RESULT.MULTI_ERROR  # 多种错误
            ):
                pass
            elif total_status == RESULT.ACCEPT:
                total_status = onecase["result"]
            else:
                total_status = RESULT.MULTI_ERROR
            
            LOGGER.debug(str(total_status))

    ret = {"submitId": submition["submitId"], "result": total_status, "case": case, "msg": "ok"}
    LOGGER.info("Judge over, return " + str(total_status))
    Return().send(ret)
    return True
