# encoding: utf-8

import json
import time
import pika

from .config import GlobalConf

from .logger import getLogger
LOGGER = getLogger(__name__)

# 单例工具
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

## 此类用于连接rabbitmq
@singleton
class RabbitmqConnecter:
    auth = connection = channel = None

    def __init__(self):
        self.queue = GlobalConf["judge queue"]
        self.username = GlobalConf["username"]
        self.password = GlobalConf["password"]
        self.host = GlobalConf["queue host"]
        self.port = GlobalConf["queue port"]

        self.__connect()
        
    def __connect(self):
        # print(host, port, username, password, self.queue)
        self.auth = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, credentials=self.auth)
        )
        if self.connection == None:
            LOGGER.error("Connect failed!")
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        LOGGER.info("Connet succeed!")

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        # LOGGER.info("Connection stop")

    def startListen(self, func):
        while True:
            try: 
                self.channel.basic_consume(self.queue, func)
                self.channel.start_consuming()
            except pika.exceptions.AMQPError:
                LOGGER.error("RabbitMQ conetcion error. Trying reconect now.")
                self.__connect()
            except BaseException as e:
                raise e
    
    def feedback(self, method):
        while True:
            try:
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
                return True
            except pika.exceptions.AMQPError:
                LOGGER.error("RabbitMQ conetcion error. Trying reconect now.")
                self.__connect()

def test_Callback(ch, method, properties, body):  # 四个参数为标准格式
    print(ch, method, properties)
    # 管道内存对象  内容相关信息 ***
    print(" [x] Received %r" % body)
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成


if __name__ == "__main__":
    queue = RabbitmqConnecter()
    queue.startListen(test_Callback)
