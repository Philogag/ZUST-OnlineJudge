import json
import time
import os
from enum import IntEnum
from threading import Thread, Lock

from .judge.local import localJudge
from .judge.vjudge import vjudge
from .Return import Return
from .RabbitMQ import RabbitmqConnecter

from .config import GlobalConf
from .static import JUDGE_METHOD, RESULT
from .logger import getLogger
LOGGER = getLogger(__name__)

class JudgeThread(RabbitmqConnecter):
    def __init__(self, threadid):
        super().__init__(threadid);
        self.thread_id = threadid

    def on_message(self, channel, method, pr, body):
        submition = json.loads(body.decode("utf-8"))

        LOGGER.info("[%d]"%self.thread_id, "Get a submition id = " + str(submition["id"]))
        Return().send({"id": submition["id"], "result": RESULT.JUDGING, "msg": ""})

        ret = {}
        try:
            if submition["judge_method"] == JUDGE_METHOD.Local:
                ret = localJudge(self.thread_id, submition)
            if GlobalConf["vjudge enabled"] \
            and submition["judge_method"] != JUDGE_METHOD.Local:
                ret = vjudge(self.thread_id, submition)

        except BaseException as e:
            ret = {"id": submition["id"], "result": RESULT.SYSTEM_ERROR, "msg": str(e)}
            LOGGER.error("[%d]"%self.thread_id, str(e))
            # raise e
        finally:
            LOGGER.info("[%d]"%self.thread_id, "Judge over, return " + str(ret["result"]))
            Return().send(ret)
            channel.basic_ack(method.delivery_tag)  # 返回完成消息至rabbitmq
