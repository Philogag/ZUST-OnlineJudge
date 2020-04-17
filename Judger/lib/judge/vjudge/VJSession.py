import requests
import base64
import json
from urllib.parse import quote
import time
from datetime import datetime, timedelta

from .LanguageMap import Language
from lib.config import GlobalConf
from lib.logger import getLogger

LOGGER = getLogger(__name__)

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class VJSession():
    session = requests.session()
    cookies = None
    cookie_time = None
    baseurl = "https://vjudge.net/"
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    def __init__(self):
        self.username = GlobalConf["vjudge username"]
        self.password = GlobalConf["vjudge password"]
        self.session = requests.Session()
        self.login()

    def login(self):
        if self.cookie_time is not None and self.cookie_time - datetime.now() < timedelta(minutes=30):
            return True
        LOGGER.info("Reset Cookies")
        header = self.headers.copy()
        header["referer"] = self.baseurl
        logindata = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(self.baseurl + "user/login", logindata, headers=header)
        
        if response.text == "success":
            self.cookie_time = datetime.now()
            self.cookies = response.cookies
            LOGGER.info("Login success.")
            return True
        else:
            raise BaseException("VJudge account login failed")
    
    # `lang` must be one of ["c", "c++", "java"] which is userd as a key at LanguageMap.py
    def submit(self, pid, lang, code):
        self.login()
        url = self.baseurl + "problem/submit"
        oj, oj_pid = pid.split("-")
        if oj not in Language.keys():
            raise RuntimeError("Unsupport OJ")
        if lang not in Language[oj].keys():
            raise RuntimeError("Unsupport Language")
        lang_code = Language[oj][lang]
        data = {
            "oj": oj,
            "probNum": oj_pid,
            "share": 0,
            "captcha": "",
            "language": lang_code,
            "source": base64.b64encode(quote(code, safe="-_.!~*'()", encoding="utf-8").encode()).decode()
        }
        header = self.headers.copy()
        header["referer"] = self.baseurl + "problem/%s-%s"%(oj,oj_pid)
        page = self.session.post(url, data, headers=header, cookies=self.cookies)
        if page.status_code == 200:
            return json.loads(page.text)["runId"]
        else:
            return -1
    
    def ask_statue(self, runId):
        url = self.baseurl + "solution/data/%d"%runId
        page = self.session.post(
            url,
            data={"showCode": "false"},
            headers={"referer": self.baseurl + "status"}
        )
        return json.loads(page.text)

