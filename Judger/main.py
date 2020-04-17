import os
import shutil  
import time
import pika


from lib.RabbitMQ import RabbitmqConnecter
from lib.JudgeManager import JudgeThread
from lib.config import GlobalConf
from lib.logger import getLogger, LogManager, LOG_LEVEL
from lib.judge.local.complie import COMPILER_USER_UID, COMPILER_GROUP_GID

# show debug info
LogManager().CONSOLE_LOG_LEVEL = LOG_LEVEL.INFO
LogManager().FILE_LOG_LEVEL = LOG_LEVEL.INFO
LogManager.SAVE_OLD_LOG = True

LOGGER = getLogger(__name__)
LOGGER.info("Server Start!")

if os.path.isdir("./temp"):
    shutil.rmtree("./temp")
os.mkdir("./temp")

ths = []
for i in range(GlobalConf["judge thread"]):
    os.mkdir("./temp/%d" % i)
    os.chown("./temp/%d" % i, COMPILER_USER_UID, COMPILER_GROUP_GID)
    ths.append(JudgeThread(i))

for th in ths:
    th.start()

for th in ths:
    th.join()

LOGGER.info("Server Stop!")

