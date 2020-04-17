# encoding: utf-8

import json
import time
import pika
from threading import Thread
from abc import abstractclassmethod

from .config import GlobalConf

from .logger import getLogger
LOGGER = getLogger(__name__)

## 此类用于连接rabbitmq
class RabbitmqConnecter(Thread):
    auth = connection = channel = None

    def __init__(self, threadid):
        super().__init__()
        self.thread_id = threadid
        self.queue = GlobalConf["judge queue"]
        self.username = GlobalConf["username"]
        self.password = GlobalConf["password"]
        self.host = GlobalConf["queue host"]
        self.port = GlobalConf["queue port"]
        
    def __connect(self):
        # print(host, port, username, password, self.queue)
        self.auth = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.auth)
        )
        if self.connection == None:
            LOGGER.error("[%d]"%self.thread_id, "Connect failed!")
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        # self.channel.confirm_delivery() # 启用
        LOGGER.info("[%d]"%self.thread_id, "Connet succeed!")

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        # LOGGER.info("Connection stop")

    def run(self):
        self.__connect()
        self.channel.basic_consume(self.queue, self.on_message)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

    @staticmethod
    def on_message(channel, method, pr, body):
        pass
