import json
import time
import os

from .complie import complie
from .compare.spj import complieSpj
from .judgeCase import JudgeCase

from lib.static import RESULT
from lib.config import GlobalConf
from lib.logger import getLogger
LOGGER = getLogger(__name__)

def localJudge(submition):
    LOGGER.info("Get a submition id = " + str(submition["id"]))

    # 尝试编译
    comp, errcode = complie(submition["lang"], submition['code'])
    if not comp:
        LOGGER.warn("Compile faild")
        return {
            "id": submition["id"],
            "result": RESULT.COMPILE_ERROR,
            "msg": "Compile faild\n" + errcode,
        }

    # 检测spj并编译，TODO
    if submition["spj"] == True:
        pass

    case = []
    total_status = RESULT.ACCEPT
    for f in os.listdir("./ProblemData/%d" % submition["pid"]):
        if f[-3:] == ".in":
            onecase = JudgeCase(
                submition,
                f[:-3],
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
    return ret
