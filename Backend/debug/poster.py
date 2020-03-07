import requests
import json

def judger_update():
    values={
        "judger-name":"172.0.0.1",
        "judger-keygen":"it is right",
    }
    

def submit():
    values={
        "pid": 1,
        "ptitle": "Local - 1 | A Test Problem",
        "contestid" : -1,
        "user": "root",
        "lang": "java",
        "code": """import java.util.*;
class Main
{
    public static void main(String args[])
    {
        Scanner cin = new Scanner(System.in);
        int a, b;
        a = cin.nextInt();
        b = cin.nextInt();
        System.out.println(a + b);
    }
}"""
    }
    response = requests.post(
        "http://localhost:8000/api/submition/new/",
        values
    )
    print(response.text)

def add_problem():
    values={
        "judge_method":0,
        "writer": "root",
        "time_limit" : 1000,
        "mem_limit": 64,
        "lang_allow": "c;c++;java;py2;py3",
        "title": "A + B Problem",
        "cont_detial" : "main field",
        "cont_input": "input field",
        "cont_output": "output field",
        "cont_hint": "hint field",
        "source": "source field",
        "tags": "debug;",
        "spj": False,
        "show_level": 1,
    }
    response = requests.post(
        "http://localhost:8000/api/problem/new/",
        values
    )
    print(response.text)


submit()
# add_problem()