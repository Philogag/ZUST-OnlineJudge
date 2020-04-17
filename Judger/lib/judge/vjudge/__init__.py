import json
from time import sleep

from .VJSession import VJSession

from lib.static import RESULT
from lib.config import GlobalConf
from lib.logger import getLogger
LOGGER = getLogger(__name__)

statusMap = {
    "AC": RESULT.ACCEPT,
    "WA": RESULT.WRONG_ANSWER,
    "TLE": RESULT.TIME_LIMIT_EXCEEDED,
    "MLE": RESULT.MEMORY_LIMIT_EXCEEDED,
    "PE": RESULT.PRESENTATION_ERROR,
    "OLE": RESULT.OUTPUT_LIMIT_EXCEEDED,
    "CE": RESULT.COMPILE_ERROR,
    "RE": RESULT.RUNTIME_ERROR,
}


def vjudge(threadid, submition):
    LOGGER.info("[%d]"%threadid, "Get a submition id = " + str(submition["id"]) + ", send to vjudge")

    runid = None
    try:
        runid = VJSession().submit(
            submition["real_pid"],
            submition["lang"],
            submition["code"]
        )
    except RuntimeError as e:
        raise RuntimeError("[%d]"% threadid + str(e))
    if runid == -1:
        raise RuntimeError("[%d]Submit Failed!" % threadid)
    
    ret = VJSession().ask_statue(runid)
    while ret["processing"]:
        sleep(1)
        ret = VJSession().ask_statue(runid)
    
    status = None
    try:
        status = statusMap[ret["statusCanonical"]]
    except KeyError:
        status = RESULT.SYSTEM_ERROR
    
    mem_use = -1
    time_use = -1
    if "memory" in ret.keys():
        mem_use = ret["memory"]
    if "runtime" in ret.keys():
        time_use = ret["runtime"]
    return {
        "id": submition["id"],
        "result": status,
        "case": json.dumps(ret),
        "msg": "ok",
        "max_mem_use_kb": mem_use,
        "max_time_use_ms": time_use,
    }