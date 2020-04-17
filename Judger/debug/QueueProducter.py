# utf-8
import pika
import json

## 此类用于连接rabbitmq
class myRabbitmqConnecter:
    connection = None

    def __init__(self):
        auth = pika.PlainCredentials("OnlineJudge", "OnlineJudge")
        self.connection = connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672, credentials=auth)
        )
        if self.connection == None:
            print("Connection failed")
            return
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="JudgeQueue", durable=True)
        print("Connection ok")

    def __del__(self):
        if self.connection != None:
            self.connection.close()
        print("Connection stop")

    def putIntoQueue(self, text):
        self.channel.basic_publish(
            exchange="",
            routing_key="JudgeQueue",
            body=text.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        print("Send a message to JudgeQueue")

code = ""
with open("/home/yhr/Desktop/t.cpp", 'r') as f:
    code = f.read()
data1 = {
    "id": 1, 
    "lang": "c++", 
    "judge_method": 0, 
    "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}", 
    "pid": 1, 
    "real_pid": "", 
    "spj": False, 
    "time_limit": 1000, 
    "mem_limit": 64
}
data2 = {
    "judge_method": 1, 
    "real_pid": "HDU-1000",
    "id": 2, 
    "lang": "c++", 
    "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\twhile(cin >> a >> b)\n\tcout << a + b << endl;\n}", 
    "pid": 2, 
    "spj": False, 
}
data3 = {
    "judge_method": 1, 
    "real_pid": "HDU-1000",
    "id": 3, 
    "lang": "c++", 
    "code": code, 
    "pid": 2, 
    "spj": False, 
}
data4 = {
    "judge_method": 1, 
    "real_pid": "HDU-1000",
    "id": 4, 
    "lang": "c++", 
    "code": "#include<iostream>\n#include<cstdio>\nint main()\n{\n\tint a,b;\n\twhile(std::cin >> a >> b)\n\tstd::cout << a + b << std::endl;\n}", 
    "pid": 2, 
    "spj": False, 
}
if __name__ == "__main__":
    ID = 0
    rmqc = myRabbitmqConnecter()
    # for i in range(10):
    # rmqc.putIntoQueue(json.dumps(data1))
    # rmqc.putIntoQueue(json.dumps(data2))
    rmqc.putIntoQueue(json.dumps(data3))
    # rmqc.putIntoQueue(json.dumps(data4))

