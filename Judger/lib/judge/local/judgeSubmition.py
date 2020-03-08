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

    case = []
    max_mem_use_kb = 0
    max_time_use_ms = 0
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
            
            max_mem_use_kb = max(max_mem_use_kb, onecase["memory"] // 1024)
            max_time_use_ms = max(max_time_use_ms, onecase["real_time"])
            LOGGER.debug(str(total_status))

    ret = {
        "id": submition["id"],
        "result": total_status,
        "case": json.dumps(case),
        "msg": "ok",
        "max_mem_use_kb":max_mem_use_kb,
        "max_time_use_ms":max_time_use_ms,
    }
    return ret
