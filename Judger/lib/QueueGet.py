# encoding: utf-8
import pika
import json
import time

from .tool.Conf import GlobalConf


from .tool.logging import getLogger
LOGGER = getLogger(__name__)

## 此类用于连接rabbitmq
class myRabbitmqConnecter:
    connection = None

    def __init__(self):
        self.queue = GlobalConf["judge queue"]
        username = GlobalConf["username"]
        password = GlobalConf["password"]
        host = GlobalConf["queue host"]
        port = GlobalConf["queue port"]

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

    def startListen(self, func):
        if self.connection == None:
            LOGGER.error("Connetion not start!")
            return
        self.channel.basic_consume(self.queue, func)
        self.channel.start_consuming()


def test_Callback(ch, method, properties, body):  # 四个参数为标准格式
    print(ch, method, properties)
    # 管道内存对象  内容相关信息 ***
    print(" [x] Received %r" % body)
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成


if __name__ == "__main__":
    queue = myRabbitmqConnecter()
    queue.startListen(test_Callback)
