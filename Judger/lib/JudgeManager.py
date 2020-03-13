import json
import time
import os
from enum import IntEnum
from threading import Thread, Lock
from queue import Queue

from .judge.local.judgeSubmition import localJudge
from .judge.hdu.judge import hdujudge
from .Return import Return
from .RabbitMQ import RabbitmqConnecter

from .config import GlobalConf
from .static import JUDGE_METHOD, RESULT
from .logger import getLogger
LOGGER = getLogger(__name__)

localjudgequeue = Queue(2)
queuelock = Lock()
_lock = False
def _setask(flag: bool):
    global _lock
    queuelock.acquire()
    global _lock
    _lock = flag
    queuelock.release()

def _asknew():
    global _lock
    queuelock.acquire()
    ret = _lock
    queuelock.release()
    return ret

def queueGetCall(ch, method, properties, body: bytes):
    # Rabbtimq 入口
    # 当 _lock == True 时将一次请求置入本地队列
    try:
        LOGGER.debug("get a submition")
        while not _asknew():
            time.sleep(0.5)
        LOGGER.debug("put into queue")
        global localJudge
        localjudgequeue.put((ch, method, properties, body))
        _setask(False)
    except BaseException as e:
        LOGGER.error("queueGetCall:", str(e))
    return True

class JudgeThread(Thread):
    def __init__(self, thid):
        super().__init__()
        self.thread_id = thid
        self.q = localjudgequeue
        self.asklock = _lock
        self.__quit_flag_lock = Lock()
        self.__quitflag = False

    def __ask_quit(self):
        self.__quit_flag_lock.acquire()
        ret = self.__quitflag
        self.__quit_flag_lock.release()
        return ret

    def callquit(self):
        self.__quit_flag_lock.acquire()
        self.__quitflag = True
        self.__quit_flag_lock.release()

    def run(self):
        LOGGER.info("Thread %d start"% self.thread_id)
        while not self.__ask_quit():
            time.sleep(0.5)
            ch = method = properties = body = None
            try:
                ch, method, properties, body = self.q.get(block=True, timeout=0.01)
            except BaseException as e:
                _setask(True)
                continue

            submition = json.loads(body.decode("utf-8"))

            LOGGER.info("Thread-%d:"%self.thread_id, "Get a submition id = " + str(submition["id"]))
            Return().send({"id": submition["id"], "result": RESULT.JUDGING, "msg": ""})

            ret = {}
            try:
                if submition["judge_method"] == JUDGE_METHOD.Local:
                    ret = localJudge(self.thread_id, submition)
                if GlobalConf["hdu enabled"] \
                and submition["judge_method"] == JUDGE_METHOD.HDU:
                    ret = hdujudge(self.thread_id, submition)

            except BaseException as e:
                ret = {"id": submition["id"], "result": RESULT.SYSTEM_ERROR, "msg": str(e)}
                LOGGER.error("Thread-%d:\n"%self.thread_id, str(e))
                # raise e
            finally:
                LOGGER.info("Thread-%d:"%self.thread_id, "Judge over, return " + str(ret["result"]))
                Return().send(ret)
                RabbitmqConnecter().feedback(method)  # 返回完成消息至rabbitmq

            _setask(True)
        LOGGER.info("Thread %d exit"% self.thread_id)

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