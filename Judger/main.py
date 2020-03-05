import os
import time
# import pika
from lib.QueueGet import myRabbitmqConnecter
from lib.Judger import *
from lib.tool.Conf import *
from lib.tool.logging import *

# show debug info
LogManager().CONSOLE_LOG_LEVEL = WARN
LogManager().FILE_LOG_LEVEL = WARN

LOGGER = getLogger(__name__)
LOGGER.info("Server Start!")

loadConf("./conf-dev.json")

if not os.path.isdir("./temp"):
    os.mkdir("./temp")
rmq = myRabbitmqConnecter()
while True:
    try:
        rmq.startListen(judgeCallback)
    except KeyboardInterrupt:
        break
    except pika.exceptions.StreamLostError:
        pass
LOGGER.info("Server Stop!")