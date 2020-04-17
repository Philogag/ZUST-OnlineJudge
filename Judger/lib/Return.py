from datetime import datetime
import requests
import json

from .logger import getLogger
from .config import GlobalConf

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

empty = {
    "case":"[]",
    "msg":"ok",
    "max_mem_use_kb":0,
    "max_time_use_ms":0
}

class Return:
    def __init__(self):
        super().__init__()
    
    def send(self, data):
        data["judger-name"] = GlobalConf["judger name"]
        data["judger-keygen"] = GlobalConf["judger keygen"]
        data["judger-time"] = datetime.timestamp(datetime.now())

        data['result'] = int(data['result'])
        for k,v in empty.items():
            if not k in data.keys():
                data[k] = v

        url = "http://" + GlobalConf["backend host"] + "/api/submition/judger/"
        
        # response = requests.post(url, data)
        # while response.status_code != 202:
        #     response = requests.post(url, data)
        print("\n" + str(data) + "\n")
