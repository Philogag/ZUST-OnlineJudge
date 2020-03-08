import json
from time import sleep

from .Session import HDUSession, lang2hdulang, str2result

from lib.static import RESULT
from lib.config import GlobalConf
from lib.logger import getLogger
LOGGER = getLogger(__name__)

def hdujudge(submition):
    LOGGER.info("Get a submition id = " + str(submition["id"]) + ", send to hdu")

    if not HDUSession().is_login():
        HDUSession.login()
        sleep(1)
    
    HDUSession().submit(
        submition["real_pid"],
        lang2hdulang(submition["lang"]),
        submition["code"]
    )

    ret = HDUSession().ask_latest_statue()
    print(ret)

    while ret["result"] in ["Queuing", "Compiling", "Running"]:
        sleep(1)
        ret = HDUSession().ask_latest_statue()
    
    return {
        "id": submition["id"],
        "result": str2result(ret["result"]),
        "case": json.dumps(ret),
        "msg": "ok",
        "max_mem_use_kb": int(ret["mem_use_kb"][:-1]),
        "max_time_use_ms": int(ret["time_use_ms"][:-2]),
    }