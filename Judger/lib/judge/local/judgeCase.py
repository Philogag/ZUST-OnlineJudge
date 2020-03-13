import json
import time
import os
import pwd
import grp

from _judger import run, UNLIMITED
from .compare.verifyManager import checkAnswer

from lib.config import GlobalConf
from lib.static import RESULT
from lib.language import LangConf
from lib.logger import getLogger
LOGGER = getLogger(__name__)

RUN_USER_UID = pwd.getpwnam("code").pw_uid
RUN_GROUP_GID = grp.getgrnam("code").gr_gid

def SystemMemeryCheck(size):  # MB
    size *= 1024
    freemem = 0
    while freemem < size + 10240: #额外10MB
        with open("/proc/meminfo", 'r') as f:
            freemem = int(f.readlines()[2].split(" ")[-2])
        time.sleep(0.2)

# 测试运行单组case文件
def JudgeCase(submition, case, basepath, threadid):
    gconf = LangConf[submition["lang"]]
    conf = LangConf[submition["lang"]]["run"]
    ret = {
        "case": case,
    }
    
    src_path = os.path.join(basepath, gconf["src_name"])
    exe_path = os.path.join(basepath, gconf["exec_name"])

    cmd = conf["cmd"] \
        .replace("{src_path}", src_path) \
        .replace("{exec_path}", exe_path) \
        .replace("exec_path_base", basepath) \
        .split(" ")

    SystemMemeryCheck(submition["mem_limit"])

    result = run(
        max_cpu_time=int(submition["time_limit"] * conf["multiplicity_time_limit"]),
        max_real_time=int(submition["time_limit"] * conf["multiplicity_time_limit"]) * 5,
        max_memory=submition["mem_limit"] * 1024 * 1024,
        max_stack=32 * 1024 * 1024,
        max_process_number=200,
        max_output_size=32 * 1024 * 1024,
        exe_path=cmd[0],
        args=cmd[1::],
        input_path= "./ProblemData/%d/%s.in" % (submition["pid"], case),
        output_path=os.path.join(basepath, "userout.txt"),
        error_path=os.path.join(basepath, "re.txt"),
        env=[],
        log_path=os.path.join(basepath, "sandbox.log"),
        seccomp_rule_name=conf["seccomp_rule"],
        uid=RUN_USER_UID,
        gid=RUN_GROUP_GID,
        memory_limit_check_only=conf["memory_limit_check_only"]
    )
    LOGGER.debug("thread-%d"%threadid, "Run return", str(result["result"]))
    
    for p, s in result.items():
        ret[p] = s
    
    if result["result"] == 1 or result["result"] == 2:
        ret["result"] = RESULT.TIME_LIMIT_EXCEEDED
    elif result["result"] == 3:
        ret["result"] = RESULT.MEMORY_LIMIT_EXCEEDED
    elif result["result"] == 4:
        ret["result"] = RESULT.RUNTIME_ERROR
    elif result["error"] != 0 or result["exit_code"] != 0:
        ret["result"] = RESULT.RUNTIME_ERROR
    elif (
        result["result"] == 0
        or (result["result"] == 5 and result["error"] == 0 and result["signal"] == 0 and result["exit_code"] == 0)
    ):
        ret["result"] = RESULT.ACCEPT
    else:
        ret["result"] = RESULT.SYSTEM_ERROR
    
    if ret["result"] != RESULT.ACCEPT:
        try:
            with open(os.path.join(basepath, "re.txt"), "r+") as f:
                ss = f.readline()
                if ss != "":
                    ret["message"] = ss
        except BaseException:
            pass
        return ret

    LOGGER.debug("thread-%d"%threadid, "Check output")

    ret["result"] = checkAnswer(submition["pid"], case, submition["spj"], basepath, threadid)

    return ret
