import re
import requests
from datetime import datetime
from enum import IntEnum

from lib.config import GlobalConf
from lib.static import RESULT

class HDU_LANG(IntEnum):
    G = 0 # g++
    GCC = 1 # gcc
    CPP = 2 # c++
    C = 3   # c
    Pascal = 4
    Java = 5
    CPPPP = 6 # C#

def lang2hdulang(lang: str):
    if lang == "c++":
        return HDU_LANG.G
    if lang == "c":
        return HDU_LANG.GCC
    if lang == "java":
        return HDU_LANG.Java
    raise Exception("Hdu system not support this language!")

def str2result(s: str):
    if s == "Accepted":
        return RESULT.ACCEPT
    if s == "Time Limit Exceeded":
        return RESULT.TIME_LIMIT_EXCEEDED
    if s == "Wrong Answer":
        return RESULT.WRONG_ANSWER
    if s == "Presentation Error":
        return RESULT.FORMAT_ERROR
    if "Runtime Error" in s:
        return RESULT.RUNTIME_ERROR
    if "Memory Limit Exceeded" == s:
        return RESULT.MEMORY_LIMIT_EXCEEDED
    if "Output Limit Exceeded" == s:
        return RESULT.WRONG_ANSWER
    if "Compilation Error" == s:
        return RESULT.COMPILE_ERROR
    raise Exception("Hdu Reult: " + s)

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class HDUSession():
    session = requests.session()
    headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    partten1 = re.compile("<tr.*?>((?:<td.*?>.*?<\/td>)*)<\/tr>")
    partten2 = re.compile("^" + ("<td.*?>(?:<.*?>)*(.*?)(?:<\/.*?>)*<\/td>" * 9))
    def __init__(self):
        self.username = GlobalConf["hdu username"]
        self.password = GlobalConf["hdu password"]

        self.login()
    
    def _post(self, url, data):
        return self.session.post(url, data, headers=self.headers)
    
    def _get(self, url):
        return self.session.get(url, headers=self.headers)

    def login(self):
        main_page = self._get("http://acm.hdu.edu.cn/").text
        loginpost = {
            "username": self.username,
            "userpass": self.password,
            "login": "Sign In"
        }
        page = self._post(
            "http://acm.hdu.edu.cn/userloginex.php?action=login",
            loginpost
        ).text

        return self.is_login()
    
    def is_login(self):
        main_page = self._get("http://acm.hdu.edu.cn/").text
        if self.username in main_page:
            return True
        else:
            return False

    def submit(self, pid, lang, code):
        url = "http://acm.hdu.edu.cn/submit.php?action=submit"
        data = {
            "check": "0",
            "problemid": pid,
            "language": int(lang),
            "usercode": code,
        }
        page = self._post(url, data)
        return page.status_code
        
    
    def ask_latest_statue(self):
        url = "http://acm.hdu.edu.cn/status.php?user=" + self.username
        # url = "http://acm.hdu.edu.cn/status.php"
        page = self._get(url).text.replace("\n", "")
        catch = re.findall(self.partten1, page)[1]
        ret = re.findall(self.partten2, catch)[0]

        return {
            'run_id': ret[0],
            'server_time': datetime.timestamp(datetime.strptime(ret[1], "%Y-%m-%d %X")),
            'result': ret[2],
            'pid': ret[3],
            'time_use_ms': ret[4],
            'mem_use_kb': ret[5],
            'code_len': ret[6],
            'lang': ret[7],
            'user': ret[8]
        }

