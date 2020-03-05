from datetime import datetime
import requests
import json

from .tool.Conf import GlobalConf

class Return:
    def __init__(self):
        super().__init__()
    
    def send(self, data):
        data["judger-name"] = GlobalConf["judger name"]
        data["judger-keygen"] = GlobalConf["judger keygen"]
        data["judger-time"] = datetime.timestamp(datetime.now())

        url = "http://" + GlobalConf["backend host"] + "/api/submition/judger"
        
        response = requests.post(url, data)
        while response.status_code != 202:
            response = requests.post(url, data)
