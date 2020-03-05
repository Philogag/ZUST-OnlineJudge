import time
from datetime import datetime
import subprocess
import os

# from ..tool.logging import getLogger
# LOGGER = getLogger(__name__)

compilecode = {
    "c": "gcc ./temp/code.c -fmax-errors=3 -o ./temp/code.out -std=c11 2>./logs/CompileError.txt",
    "c++": "g++ ./temp/code.cpp -fmax-errors=3 -o ./temp/code.out -std=c++11 2>./logs/CompileError.txt",
    "py3": "python3 -m py_compile ./temp/code.py 2>./logs/CompileError.txt",
    "py2": "python2 -m py_compile ./temp/code.py 2>./logs/CompileError.txt",
    "java": "javac ./temp/Main.java -d temp 2>./logs/CompileError.txt",
}


def compileFile(lang):
    try:
        result = subprocess.run(
            compilecode[lang].replace("./", __file__[:-22]), timeout=10, shell=True
        )  # 硬编码，相对路径改绝对路径，修改文件与文件夹需注意
    except BaseException as e:
        if e == subprocess.TimeoutExpired:
            return (False, "Compile Timeout!")
        else:
            return (False, "Compile error")
    if result.returncode != 0:
        try:
            with open("./logs/CompileError.txt", "r") as f:
                s = f.read()
                return (False, "Compile Error!\n" + s)
        except BaseException:
            pass
        return (False, "Compile error because of unkown reason")
    return (True, None)


if __name__ == "__main__":
    print(compileFile("c++"))
    print(compileFile("java"))
    print(compileFile("py2"))
