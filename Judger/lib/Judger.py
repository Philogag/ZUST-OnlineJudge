import json
import time
import os

from .tool.Conf import GlobalConf
from .judge.localjudge.judgeSubmition import *


from .tool.logging import getLogger
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


def judgeCallback(ch, method, properties, body: bytes):
    # 此函数用于处理队列消息
    # ch为队列管道，用于返回处理信号
    # body为消息本体

    submition = json.loads(body.decode("utf-8"))
    if submition["judger"] == 'Local':
        localJudge(submition)

    ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回完成消息至rabbitmq
    return True
