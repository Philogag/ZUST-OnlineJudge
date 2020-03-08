import json
import socket
import os
import re

# from .logging import getLogger
# LOGGER = getLogger(__name__)

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
    # ----------------------
    #   HDU judger
    "hdu enabled": False,
}

# main.py 的绝对路径
GlobalConf["path"] = re.match("(.*?/)lib.*?", __file__).group()[:-3]

def __init():
    ENABLE_GLOBAL_CONF = True
    conf = {}
    with open(os.path.join(GlobalConf["path"], 'conf.json'), "r") as f:
        conf = json.load(f)

    for p, s in conf.items():
        GlobalConf[p] = s
    

__init()