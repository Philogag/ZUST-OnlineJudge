import json
import time
import os
from enum import IntEnum

from .tool.Conf import GlobalConf
from .judge.localjudge.judgeSubmition import *


from .tool.logging import getLogger
LOGGER = getLogger(__name__)

class JUDGE_METHOD(IntEnum):
    Local = 0
    HDU = 1
    Codeforce = 2

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



def judgeCallback(ch, method, properties, body: bytes):
    # 此函数用于处理队列消息
    # ch为队列管道，用于返回处理信号
    # body为消息本体

    submition = json.loads(body.decode("utf-8"))
    if submition["judge_method"] == JUDGE_METHOD.Local:
        localJudge(submition)

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回完成消息至rabbitmq
    return True
