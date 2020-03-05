import requests
import json

def judger_update():
    values={
        "judger-name":"172.0.0.1",
        "judger-keygen":"it is right",
    }  
    

def submit():
    values={
        "judge_method":"local",
        "pid": 1,
        "ptitle": "Local - 1 | A Test Problem",
        "contestid" : -1,
        "username": "root",
        "lang": "c++",
        "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}"
    }
    response = requests.post(
        "http://localhost:8000/api/submition/new/",
        values
    )
    print(response.text)

submit()



# print(judger_update())