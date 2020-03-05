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

    def putIntoQueue(self, text, queue):
        self.channel.basic_publish(
            exchange="",
            routing_key="JudgeQueue",
            body=text.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        print("Send a message to JudgeQueue")


globaldir = {
    "time_lim": 1000,
    "mem_lim": 64,
    "spj": False,
    "submitId": 1,
    "problemId": 1,
    "judger": "Local",
}

ID = 0

def sid():
    global ID
    ID += 1
    return ID

## 此函数将产生json
def createCPP():
    r = globaldir.copy()
    r["submitId"] = sid()
    r["lang"] = "c++11"
    r[
        "code"
    ] = """#include <iostream>
using namespace std;
int main()
{
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
}"""
    return json.dumps(r)


def createJAVA():
    r = globaldir.copy()
    r["submitId"] = sid()
    r["lang"] = "java"
    r[
        "code"
    ] = """import java.util.*;
public class Main
{
    public static void main(String args[])
    {
        int[] x = new int[5000000];
        Scanner cin = new Scanner(System.in);
        int a, b;
        a = cin.nextInt();
        b = cin.nextInt();
        System.out.println(a + b);
    }
}"""
    return json.dumps(r)


def createPY3():
    r = globaldir.copy()
    r["submitId"] = sid()
    r["lang"] = "python3"
    r[
        "code"
    ] = """a, b = input().split(" ")
print(int(a) + int(b))
"""
    return json.dumps(r)


if __name__ == "__main__":
    ID = 0
    rmqc = myRabbitmqConnecter()
    for i in range(10):
        rmqc.putIntoQueue(createCPP(), "Local")
        # rmqc.putIntoQueue(createJAVA(), "Local")
        rmqc.putIntoQueue(createPY3(), "Local")

