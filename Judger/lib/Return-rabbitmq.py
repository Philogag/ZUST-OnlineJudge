# 此文件已废弃

import pika
import json
import time
from datetime import datetime

from .tool.Conf import GlobalConf

from .tool.logging import getLogger
LOGGER = getLogger(__name__)

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# 单例模式类
# 用于返回测评状态
@singleton
class Return:
    connection = None

    def __init__(self,):
        self.queue = GlobalConf["ReturnQueue"]
        username = GlobalConf["username"]
        password = GlobalConf["password"]
        host = GlobalConf["host"]
        port = GlobalConf["port"]

        # print(host, port, username, password, self.queue)
        auth = pika.PlainCredentials(username, password)
        self.connection = connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=auth)
        )
        if self.connection == None:
            LOGGER.error("Connection failed!")
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        LOGGER.info("Connetion succeed!")

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        # LOGGER.info("Connection stop")

    def send(self, dic):
        dic["judger-name"] = GlobalConf["server name"]
        dic["judger-time"] = datetime.timestamp(datetime.now())

        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(dic),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
