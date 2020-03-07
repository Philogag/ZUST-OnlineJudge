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
        self.username = RABBITMQ_USER
        self.password = RABBITMQ_PASS
        self.host = RABBITMQ_HOST
        self.port = RABBITMQ_PORT

        self.auth = pika.PlainCredentials(self.username, self.password)
        self.connection = connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.auth)
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
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(dict(data)),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
        except BaseException:
            self.connection = connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.auth)
            )
            self.channel = self.connection.channel()
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(dict(data)),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
