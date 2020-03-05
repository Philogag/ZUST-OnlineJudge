import pika
import json
import time
from datetime import datetime

from Backend.settings import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER, QUEUE_NAME


# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# 单例模式
# 用于注入rabbitmq
@singleton
class RabbitMQ:
    connection = None

    def __init__(self,):
        self.queue = QUEUE_NAME
        username = RABBITMQ_USER
        password = RABBITMQ_PASS
        host = RABBITMQ_HOST
        port = RABBITMQ_PORT

        auth = pika.PlainCredentials(username, password)
        self.connection = connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=auth)
        )
        if self.connection == None:
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        # LOGGER.info("Connection stop")

    def put(self, data):
        """
        单次置入数据
        """
        pass
