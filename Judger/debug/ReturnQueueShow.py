import pika
import json
import time
from datetime import datetime
from enum import IntEnum

class RESULT(IntEnum):
    ACCEPT = 0
    COMPILE_ERROR = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    FORMAT_ERROR = 6
    WRONG_ANSWER = 7
    MULTI_ERROR = 8

    JUDGING = -1

## 此类用于连接rabbitmq
class myRabbitmqConnecter:
    connection = None

    def __init__(self):
        self.queue = "ReturnQueue"
        username = "OnlineJudge"
        password = "OnlineJudge"
        host = "localhost"
        port = 5672

        # print(host, port, username, password, self.queue)
        auth = pika.PlainCredentials(username, password)
        self.connection = connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=auth)
        )
        if self.connection == None:
            print("Connection failed!")
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        print("Connetion succeed!")

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        print("Connection stop")

    def startListen(self, func):
        if self.connection == None:
            print("Connetion not start!")
            return
        self.channel.basic_consume(self.queue, func)
        self.channel.start_consuming()


def testCallback(ch, method, properties, body):  # 四个参数为标准格式
    ret = json.loads(body.decode("utf-8"))
    ss = "[%s][ID:%d][%s]: %s" % (
        datetime.fromtimestamp(ret["server-time"]).strftime("%Y-%m-%d %H:%M:%S %f"),
        ret["submitId"],
        ret["server-name"],
        RESULT(ret["result"]) 
    )
    print(ss)
    time.sleep(1)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成


if __name__ == "__main__":
    queue = myRabbitmqConnecter()
    queue.startListen(testCallback)
