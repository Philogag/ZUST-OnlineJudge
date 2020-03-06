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

def localJudge(submition):
    LOGGER.info("Get a submition id = " + str(submition["id"]))
    Return().send({"id": submition["id"], "result": RESULT.JUDGING, "msg": ""})

    # 检测语言种类
    if not submition["lang"] in GlobalConf["avaid lang"]:
        LOGGER.warn("Code language type not found")
        Return().send(  # 此处返回 System Error
            {
                "id": submition["id"],
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
                "id": submition["id"],
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
                "id": submition["id"],
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
    for f in os.listdir("./ProblemData/%d" % submition["pid"]):
        if f[-3:] == ".in":
            onecase = JudgeCase(
                submition["pid"],
                f[:-3],
                submition["spj"],
                submition["time_limit"],
                submition["mem_limit"],
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

    ret = {"id": submition["id"], "result": total_status, "case": json.dumps(case), "msg": "ok"}
    LOGGER.info("Judge over, return " + str(total_status))
    Return().send(ret)
    return True
