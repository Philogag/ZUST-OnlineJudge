import os
import json
import pwd
import grp

from _judger import run, RESULT_SUCCESS, UNLIMITED

from lib.Errors import *
from lib.logger import getLogger
from lib.config import GlobalConf
from lib.language import LangConf
LOGGER = getLogger(__name__)

COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

complie_error_out = os.path.join(GlobalConf["path"], "logs", "CompileError.txt")

def complie(lang, code) -> (bool, str):
    if not lang in LangConf.keys():
        return (False, "Language Not Support!")
    langconf = LangConf[lang]
    src_path = langconf["src_name"]
    try:
        with open(src_path, 'w+') as f:
            f.writelines(code)
    except BaseException as e:
        return (False, str(e))
    langconf = langconf["complie"]

    print(langconf["cmd"])

    cmd = langconf["cmd"].split(" ")

    max_memory_mb = langconf["max_memory_mb"] * 1024 * 1024
    if max_memory_mb < 0:
        max_memory_mb = UNLIMITED

    result = run(
        max_cpu_time=langconf["max_cpu_time_ms"],
        max_real_time=langconf["max_real_time_ms"],
        max_memory=max_memory_mb,
        max_stack=32 * 1024 * 1024,
        max_process_number=UNLIMITED,
        max_output_size=32 * 1024 * 1024,
        exe_path=cmd[0],
        args=cmd[1::],             
        input_path='/dev/null',
        output_path=complie_error_out,
        error_path=complie_error_out,
        env=["PATH=" + os.getenv("PATH")],
        log_path="./logs/sandbox.log",
        seccomp_rule_name=None,
        uid=COMPILER_USER_UID,
        gid=COMPILER_GROUP_GID
    )

    if result["result"] != RESULT_SUCCESS:
        if os.path.exists(complie_error_out):
            with open(complie_error_out, encoding="utf-8") as f:
                error = f.read().strip()
                os.remove(complie_error_out)
                if error:
                    return (False, error)
        return (False, "Compiler runtime error, info: %s" % json.dumps(result))
    else:
        try:
            os.remove(complie_error_out)
        except FileNotFoundError:
            pass
        return (True, "")


