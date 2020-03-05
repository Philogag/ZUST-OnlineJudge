import os
import time
from datetime import datetime

global DEBUG
global INFO
global WARN
global ERROR
DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# 单例模式类
# 用于返回测评状态
@singleton
class LogManager():
    colordir = {
        "{$red}": "\033[1;31m",
        "{$green}": '\033[1;32m',
        "{$yellow}": '\033[1;33m',
        "{$}": '\033[0m',
    }
    levelstrc = (
        '\033[0mDEBUG', # white
        '\033[1;32mINFO\033[0m', # green
        '\033[1;33mWARN\033[0m', # yellow
        '\033[1;31mERROR\033[0m', # red
    )
    levelstr = (
        'DEBUG', # white
        'INFO', # green
        'WARN', # yellow
        'ERROR', # red
    )

    log_path = "./logs"
    latest_log = "latest-system.log"

    FILE_LOG_LEVEL = INFO
    CONSOLE_LOG_LEVEL = INFO
    SAVE_OLD_LOG = False

    def __init__(self):
        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)
        
        self.latest_log = os.path.join(self.log_path, self.latest_log)

        if self.SAVE_OLD_LOG and os.path.isfile(self.latest_log):
            ftime = os.path.getmtime(self.latest_log)
            ename = time.strftime("%y-%m-%d-%H-%M-%S-", time.localtime(ftime)) + "system.log"
            os.rename(self.latest_log, os.path.join(self.log_path, ename))
        with open(self.latest_log, "w+") as f:
            pass
    
    def __del__(self):
        pass
    
    def put(self, logs: str, owner, level:int):
        timestamp = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        if owner == None:
            owner = "None"
        fowner = owner
        flogs = logs
        for l, r in self.colordir.items():
            owner = owner.replace(l, r)
            logs = logs.replace(l, r)
            fowner = fowner.replace(l, "")
            flogs = flogs.replace(l, "")
        
        if level >= self.CONSOLE_LOG_LEVEL:
            print("[" + timestamp + "][" + self.levelstrc[level] + "][" + owner + "]:", logs)
        if level >= self.FILE_LOG_LEVEL:
            try:
                with open(self.latest_log, "a") as f:
                    f.writelines(
                        "[" + timestamp + "][" + self.levelstr[level] + "][" + fowner + "]: " + flogs + "\n"
                    )
            except BaseException:
                pass

class Logger():
    manage = LogManager()
    def __init__(self, name):
        self.name = name
    def error(self, msg:str):
        self.manage.put(msg, self.name, ERROR)
    def warn(self, msg: str):
        self.manage.put(msg, self.name, WARN)
    def info(self, msg: str):
        self.manage.put(msg, self.name, INFO)
    def debug(self, msg: str):
        self.manage.put(msg, self.name, DEBUG)

def getLogger(name = __name__):
    return Logger(name)

if __name__ == "__main__":
    LogManager().consile_log_level = DEBUG

    LOGGER = getLogger()
    LOGGER.error("error")
    LOGGER.warn("warn")
    LOGGER.info("info")
    LOGGER.debug("debug")