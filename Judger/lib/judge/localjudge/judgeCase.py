import json
import time
import os
from enum import IntEnum
import subprocess

from _judger import run
from ...compare import *

from ...tool.Conf import GlobalConf
from ...tool.logging import getLogger
LOGGER = getLogger(__name__)

class RESULT(IntEnum):
    ACCEPT = 0
    COMPILE_ERROR = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    FORMAT_ERROR = 6
    WRONG_ANSWER = 7
    MULTI_ERROR = 8

    JUDGING = -1

def SystemMemeryCheck(size):  # MB
    size *= 1024
    freemem = 0
    while freemem < size + 10240: #额外10MB
        with open("/proc/meminfo", 'r') as f:
            freemem = int(f.readlines()[2].split(" ")[-2])
        time.sleep(0.2)

# 测试运行单组case文件
def JudgeCase(pid, prefixname, isspj, time_lim, mem_lim, lang):
    ret = {
        "case": prefixname,
    }
    args = []
    if lang == "py2" or lang == "py3":
        args = ["./temp/code.py"]
    
    SystemMemeryCheck(mem_lim)

    get = {}
    if lang == "java":
        get = JavaJudgeCase(pid,prefixname,time_lim,mem_lim)
    else:
        get = run(
            max_cpu_time=time_lim,
            max_real_time=time_lim * 10,
            max_memory=mem_lim * 1024 * 1024,
            max_stack=32 * 1024 * 1024,
            max_process_number=200,
            max_output_size=32 * 1024 * 1024,
            exe_path={
                "c": "./temp/code.out",
                "c++": "./temp/code.out",
                "java": GlobalConf["JavaPath"],
                "py2": GlobalConf["Python2Path"],
                "py3": GlobalConf["Python3Path"],
            }[lang],
            input_path="./ProblemData/%d/%s.in" % (pid, prefixname),
            output_path="./temp/userout.txt",
            error_path="./logs/RunTimeError.txt",
            args=args,
            env=[],
            log_path="./logs/Sandbox.log",
            seccomp_rule_name={
                "py2": "general",
                "py3": "general",
                "java": "general",
                "c": "general",
                "c++": "general",
            }[lang],
            uid=0,
            gid=0,
        )
    LOGGER.debug(str(get["result"]))
    
    for p, s in get.items():
        ret[p] = s
    
    if get["result"] == 1 or get["result"] == 2:
        ret["result"] = RESULT.TIME_LIMIT_EXCEEDED
    elif get["result"] == 3:
        ret["result"] = RESULT.MEMORY_LIMIT_EXCEEDED
    elif get["result"] == 4:
        ret["result"] = RESULT.RUNTIME_ERROR
    elif get["error"] != 0 or get["exit_code"] != 0:
        ret["result"] = RESULT.RUNTIME_ERROR
    elif (
        get["result"] == 0
        or (get["result"] == 5 and get["error"] == 0 and get["signal"] == 0 and get["exit_code"] == 0)
    ):
        ret["result"] = RESULT.ACCEPT
    else:
        ret["result"] = RESULT.SYSTEM_ERROR
    
    if ret["result"] != RESULT.ACCEPT:
        try:
            with open("./logs/RunTimeError.txt", "r+") as f:
                ss = f.readline()
                if ss != "":
                    ret["message"] = ss
        except BaseException:
            pass
        return ret

    LOGGER.debug("Check output")
    dif = compareMain("./temp/userout.txt", "./ProblemData/%d/%s.out" % (pid, prefixname),)
    
    if dif == 0:
        ret["result"] = RESULT.ACCEPT
    elif dif == 1:
        ret["result"] = RESULT.FORMAT_ERROR # 格式错误
    elif dif == 2:
        ret["result"] = RESULT.WRONG_ANSWER  # WA
    else:
        ret["result"] = RESULT.SYSTEM_ERROR
    return ret

def JavaJudgeCase(pid, prefixname, time_lim, mem_lim):
    args = [
        GlobalConf["JavaPath"],
        "-cp", GlobalConf["path"] + "temp/",
        "-Xmx" + str(mem_lim) + "m",
        "-XX:PermSize=" + str(mem_lim // 2) + "m",
        "-XX:MaxPermSize=" + str(mem_lim) + "m",
        "-Djava.security.manager",
        "Main",
    ]
    exit_code = 0
    try:
        stdin = open("./ProblemData/%d/%s.in" % (pid, prefixname), 'r')
        stdout = open("./temp/userout.txt", 'w+')
        stderr = open("./logs/RunTimeError.txt", "w+")
        with subprocess.Popen(
            args,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr
        ) as pipe:
            try:
                pipe.wait(timeout=int(time_lim * GlobalConf["java time"]))
            except subprocess.TimeoutExpired: # 超时
                pipe.kill()
            exit_code = pipe.returncode
        stdin.close()
        stdout.close()
        stderr.close()
    except BaseException:
        stdin.close()
        stdout.close()
        stderr.close()
    LOGGER.debug("java exit:" + str(exit_code))
    return {
        "result": 0,
        "error": 0,
        "exit_code": exit_code
    }