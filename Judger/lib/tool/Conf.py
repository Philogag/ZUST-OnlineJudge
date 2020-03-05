import json
import socket
import os
import re

# from .logging import getLogger
# LOGGER = getLogger(__name__)

global GlobalConf
GlobalConf = {
    # ----------------------
    #   System Config
    "judger name": socket.gethostbyname(socket.gethostname()),
    "judger keygen": "",
    "queue host": "localhost",
    "queue port": 5672,
    "username": "guest",
    "password": "guest",
    "judge queue": "LocalJudgeQueue",
    "ReturnQueue": "ReturnQueue",
    # ----------------------
    #   Compiler Config
    "java time": 2,
    "JavaPath": "/usr/bin/java",
    "Python2Path": "/usr/bin/python",
    "Python3Path": "/usr/bin/python3",
}

# main.py 的绝对路径
GlobalConf["path"] = re.match("(.*?/)lib.*?", __file__).group()[:-3]

def loadConf(file=None):
    ENABLE_GLOBAL_CONF = True
    conf = {}
    if file != None and os.path.isfile(file):
        with open(file, "r") as f:
            conf = json.load(f)

    for p, s in conf.items():
        GlobalConf[p] = s
    

