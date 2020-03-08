import json
import time
import os
from enum import IntEnum

from .judge.local.judgeSubmition import localJudge
from .judge.hdu.judge import hdujudge
from .Return import Return

from .config import GlobalConf
from .static import JUDGE_METHOD, RESULT
from .logger import getLogger
LOGGER = getLogger(__name__)

def judgeManager(ch, method, properties, body: bytes):
    # 此函数用于处理队列消息
    # ch为队列管道，用于返回处理信号
    # body为消息本体

    submition = json.loads(body.decode("utf-8"))

    Return().send({"id": submition["id"], "result": RESULT.JUDGING, "msg": ""})

    ret = {}
    try:
        if submition["judge_method"] == JUDGE_METHOD.Local:
            ret = localJudge(submition)
        if GlobalConf["hdu enabled"] \
           and submition["judge_method"] == JUDGE_METHOD.HDU:
            ret = hdujudge(submition)


    except BaseException as e:
        ret = {"id": submition["id"], "result": RESULT.SYSTEM_ERROR, "msg": str(e)}
        LOGGER.error(str(e))
        raise e
    finally:
        LOGGER.info("Judge over, return " + str(ret["result"]))
        Return().send(ret)

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回完成消息至rabbitmq
    return True

"""
{
    id,
    result,
    case,
    msg,
    max_mem_use_kb,
    max_time_use_ms
}
"""