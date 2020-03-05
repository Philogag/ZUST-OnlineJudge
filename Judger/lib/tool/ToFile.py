import os
import sys

from .logging import getLogger
LOGGER = getLogger(__name__)

filename = {
    "c": "code.c",
    "c++": "code.cpp",
    "java": "Main.java",
    "py2": "code.py",
    "py3": "code.py",
}


def toFile(lang, text):
    if os.path.isdir("./temp"):
        os.system("rm -rf ./temp")
    os.makedirs("./temp/")
    with open("./temp/" + filename[lang], "w+", encoding="utf-8") as f:
        f.writelines(text)
    return True
