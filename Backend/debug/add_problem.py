import requests
import json

def add_problem():
    values={
        "judge_method": 1,
        "real_pid": "1000",
        "writer": "root",
        "time_limit" : 1000,
        "mem_limit": 64,
        "lang_allow": "c;c++;java;py2;py3",
        "title": "Spj test problem",
        "cont_detial" : "main field",
        "cont_input": "input field",
        "cont_output": "output field",
        "cont_hint": "hint field",
        "source": "source field",
        "tags": "debug;",
        "spj": True,
        "show_level": 1,
    }
    response = requests.post(
        "http://localhost:8000/api/problem/new/",
        values
    )
    print(response.text)

add_problem()