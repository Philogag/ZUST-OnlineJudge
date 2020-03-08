import os
import difflib
import pwd
import grp

from _judger import run, UNLIMITED, RESULT_SUCCESS

from lib.language import SpjConf
from lib.config import GlobalConf
from lib.static import RESULT
from lib.logger import getLogger
LOGGER = getLogger(__name__)

SPJ_USER_UID = pwd.getpwnam("spj").pw_uid
SPJ_GROUP_GID = grp.getgrnam("spj").gr_gid

def spjChecker(pid, caseid):

    ret, msg = complieSpj(pid)
    if not ret:
        raise Exception("Spjudge complie error\n" + msg)

    spjconf = SpjConf["spj"]["run"]
    spjlog = os.path.join(GlobalConf["path"], "logs", "spjrun.log")
    
    efile = os.path.join(GlobalConf["path"], "Spj/%d"%pid)
    ifile = os.path.join(GlobalConf["path"], "ProblemData/%d/%s.in"%(pid, caseid))
    uofile = os.path.join(GlobalConf["path"], "temp/userout.txt")
    cmd = spjconf["cmd"]

    cmd = cmd.replace("{exec_path}", efile) \
             .replace("{infile_path}", ifile) \
             .replace("{user_out_file_path}", uofile) \
             .split(" ")

    result = run(
        exe_path=cmd[0],
        args=cmd[1::],
        max_cpu_time=spjconf["max_cpu_time_ms"],
        max_real_time=spjconf["max_real_time_ms"],
        max_memory=spjconf["max_memory_mb"] * 1024 * 1024,
        max_process_number=UNLIMITED,
        max_stack=32 * 1024 * 1024,
        max_output_size=64 * 1024 * 1024,
        input_path='/dev/null',
        output_path=spjlog,
        error_path=spjlog,
        env=[],
        log_path=spjlog,
        seccomp_rule_name=None,
        uid=SPJ_USER_UID,
        gid=SPJ_GROUP_GID
    )
    try:
        os.remove(spjlog)
    except FileNotFoundError:
        pass
    if result["result"] == 0:
        return RESULT.ACCEPT
    elif result["result"] == 1:
        return RESULT.WRONG_ANSWER
    else:
        raise Exception("Spjudge runtime error!")


def complieSpj(pid):
    spjconf = SpjConf["spj"]

    ifile = os.path.join(GlobalConf["path"], "Spj/%d.cpp"%(pid))
    ofile = os.path.join(GlobalConf["path"], "Spj/%d"%pid)

    spjconf = spjconf["complie"]

    cmd = spjconf["cmd"]

    cmd = cmd.replace("{src_path}", ifile) \
             .replace("{exec_path}", ofile) \
             .split(" ")

    if not os.path.isfile(ifile):
        return False, "Spj file not exist"
    
    if os.path.isfile(ofile):
        return True, None

    spjlog = os.path.join(GlobalConf["path"], "logs", "spjcomplie.log")

    result = run(
        exe_path=cmd[0],
        args=cmd[1::],
        max_cpu_time=spjconf["max_cpu_time_ms"],
        max_real_time=spjconf["max_real_time_ms"],
        max_memory=spjconf["max_memory_mb"] * 1024 * 1024,
        max_process_number=UNLIMITED,
        max_stack=32 * 1024 * 1024,
        max_output_size=64 * 1024 * 1024,
        input_path='/dev/null',
        output_path=spjlog,
        error_path=spjlog,
        env=["PATH=" + os.getenv("PATH")],
        log_path=spjlog,
        seccomp_rule_name=None,
        uid=SPJ_USER_UID,
        gid=SPJ_GROUP_GID
    )

    if result["result"] != RESULT_SUCCESS:
        if os.path.exists(spjlog):
            with open(spjlog, encoding="utf-8") as f:
                error = f.read().strip()
                os.remove(spjlog)
                if error:
                    return (False, error)
        return (False, "Compiler runtime error, info: %s" % json.dumps(result))
    else:
        try:
            os.remove(spjlog)
        except FileNotFoundError:
            pass
        return (True, "")


if __name__ == "__main__":
    print(spjChecker("./temp/userout.txt", "./ProblemData/1/1.out"))

