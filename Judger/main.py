import os
import time
import pika

from lib.RabbitMQ import RabbitmqConnecter
from lib.JudgeManager import judgeManager
from lib.config import GlobalConf
from lib.logger import getLogger, LogManager, LOG_LEVEL


# show debug info
LogManager().CONSOLE_LOG_LEVEL = LOG_LEVEL.DEBUG
LogManager().FILE_LOG_LEVEL = LOG_LEVEL.INFO

LOGGER = getLogger(__name__)
LOGGER.info("Server Start!")

if not os.path.isdir("./temp"):
    os.mkdir("./temp")
rmq = RabbitmqConnecter()
while True:
    try:
        rmq.startListen(judgeManager)
    except KeyboardInterrupt:
        break
    except pika.exceptions.StreamLostError:
        pass
LOGGER.info("Server Stop!")