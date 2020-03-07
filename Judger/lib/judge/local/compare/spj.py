import os
import difflib
import pwd
import grp

from lib.logger import getLogger
LOGGER = getLogger(__name__)

SPJ_USER_UID = pwd.getpwnam("spj").pw_uid
SPJ_GROUP_GID = grp.getgrnam("spj").gr_gid

def spjChecker(pid, caseid):
    pass

def complieSpj(pid):
    pass

if __name__ == "__main__":
    print(spjChecker("./temp/userout.txt", "./ProblemData/1/1.out"))

