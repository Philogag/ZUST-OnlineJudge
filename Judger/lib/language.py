import json
import os

from .logger import getLogger
from .config import GlobalConf

LangConf = {}
SpjConf = {}

## default settings
lang_ds = {
    "name": "",
    "src_name": "",
    "exec_name": "",
    "complie": {
        "max_cpu_time_ms": 3000,
        "max_real_time_ms": 5000,
        "max_memory_mb": -1,
        "compile_command": ""
    },
    "run": {
        "command": "",
        "seccomp_rule": None,
        "memory_limit_check_only": 1,
        "multiplicity_time_limit": 1
    }
}

def _init():
    confs = None
    with open(os.path.join(GlobalConf["path"], "language.json"), 'r') as f:
        confs = json.load(f)
        getLogger(__name__).info("Load language settings.")
    
    for c in confs:
        if "spj" in c["name"]:
            SpjConf[c["name"]] = c
        else:
            for ii in lang_ds["complie"].keys():
                if not ii in c["complie"].keys():
                    c["complie"][ii] = lang_ds["complie"][ii]
            for ii in lang_ds["run"].keys():
                if not ii in c["run"].keys():
                    c["run"][ii] = lang_ds["run"][ii]
            LangConf[c["name"]] = c

_init()