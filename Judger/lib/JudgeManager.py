import json
import time
import os
from enum import IntEnum

from .judge.local.judgeSubmition import localJudge
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
    if submition["judge_method"] == JUDGE_METHOD.Local:
        ret = localJudge(submition)

    Return().send(ret)

    # ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回完成消息至rabbitmq
    return True
