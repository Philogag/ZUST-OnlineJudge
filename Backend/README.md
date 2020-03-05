## 目录
- [目录](#%e7%9b%ae%e5%bd%95)
- [接口](#%e6%8e%a5%e5%8f%a3)
  - [Submition](#submition)
    - [Static Value](#static-value)
    - [`/api/submition/all/` GET](#apisubmitionall-get)
    - [`/api/submition/(\d+)/` GET](#apisubmitiond-get)
    - [`/api/submition/new` POST](#apisubmitionnew-post)
  - [Problem](#problem)
    - [Static Value](#static-value-1)
    - [`/api/problem/all/` GET](#apiproblemall-get)
    - [`/api/problem/(\d+)/` GET](#apiproblemd-get)
    - [`/api/problem/new/` POST](#apiproblemnew-post)

---
## 接口

### Submition 

#### Static Value
Statues Code
+ ACCEPT = 0
+ COMPILE_ERROR = 1
+ TIME_LIMIT_EXCEEDED = 2
+ MEMORY_LIMIT_EXCEEDED = 3
+ RUNTIME_ERROR = 4
+ SYSTEM_ERROR = 5
+ FORMAT_ERROR = 6
+ WRONG_ANSWER = 7
+ MULTI_ERROR = 8
+ JUDGING = -1
+ WAITING = -2

#### `/api/submition/all/` GET
提交列表
Return:
```json
[
  {"id": 1, "pid": 1, "ptitle": "Local - 1 | A Test Problem", "contestid": -1, "user": "root", "timestamp": "2020-03-05T03:29:16.840304Z", "lang": "c++", "statue": -2, "judger": "localhost"},
  ...
]
```

#### `/api/submition/(\d+)/` GET
提交详情
Return:
```json
{"id": 1, "pid": 1, "ptitle": "Local - 1 | A Test Problem", "contestid": -1, "user": "root", "timestamp": "2020-03-05T03:29:16.840304Z", "lang": "c++", "code": "code", "statue": -2, "judger": "localhost", "statue_detail": "", "judger_msg": ""}
```

#### `/api/submition/new` POST
新建提交，并判题
POST:
```json
{
  "pid": 1, // problem id, the problem must be exist
  "ptitle": "Local - 1 | A + B Problem",
  "contestid" : -1, // -1 means public
  "user": "root",
  "lang": "c++",
  "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}"
}
```
Return:
```json
{"id": 1, "pid": 1, "ptitle": "Local - 1 | A Test Problem", "contestid": -1, "user": "root", "timestamp": "2020-03-05T03:32:33.384803Z", "lang": "c++", "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}", "statue": -2, "judger": "localhost", "statue_detail": "", "judger_msg": ""}
```
Put into rabbtimq:
```json
{"id": 1, "lang": "c++", "judge_method": 0, "contestid": -1, "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}", "pid": 1, "real_pid": -1, "spj": false, "time_limit": 1000, "mem_limit": 64}
```

---
### Problem

#### Static Value


Judge Method:
+ Local = 0
+ HDU = 1
+ Codeforce = 2

Show Level:
+ Hide = 0
+ Show = 1
+ In contest = 2

#### `/api/problem/all/` GET
题库
Return:
```json
[
  {"id": 1, "judge_method": 0, "real_pid": -1, "writer": "root", "last_edit": "2020-03-05T02:50:21.738491Z", "time_limit": 1000, "mem_limit": 64, "lang_allow": "c;c++;java;py2;py3", "title": "A + B Problem", "cont_detial": "main field", "cont_input": "input field", "cont_output": "output field", "cont_hint": "hint field", "source": "source field", "tags": "debug;", "spj": false, "show_level": 1}
  ...
]
```

#### `/api/problem/(\d+)/` GET
题面
Return:
```json
{"id": 1, "judge_method": 0, "real_pid": -1, "writer": "root", "last_edit": "2020-03-05T02:50:21.738491Z", "time_limit": 1000, "mem_limit": 64, "lang_allow": "c;c++;java;py2;py3", "title": "A + B Problem", "cont_detial": "main field", "cont_input": "input field", "cont_output": "output field", "cont_hint": "hint field", "source": "source field", "tags": "debug;", "spj": false, "show_level": 1, "tot_cnt": 0, "ac_cnt": 0, "wa_cnt": 0, "tle_cnt": 0, "mle_cnt": 0, "ce_cnt": 0, "se_cnt": 0, "re_cnt": 0, "me_cnt": 0}
```
#### `/api/problem/new/` POST
添加/修改题目
POST:
```json
{
  "judge_method":0, 
  "real_pid": -1, // When judge in local, this value is useless
  "writer": "root",
  "time_limit" : 1000,
  "mem_limit": 64,
  "lang_allow": "c;c++;java;py2;py3", // split with `;`
  "title": "",
  "cont_detial" : "",
  "cont_input": "",
  "cont_output": "",
  "cont_hint": "",
  "source": "",
  "tags": "tagA;tagB", // split with `;`
  "spj": false, // or true
  "show_level": 1,
}
```
Return:
```json
Succeed: 201
{"id": 1, "judge_method": 0, "real_pid": -1, "writer": "root", "last_edit": "2020-03-05T02:50:21.738491Z", "time_limit": 1000, "mem_limit": 64, "lang_allow": "c;c++;java;py2;py3", "title": "A + B Problem", "cont_detial": "main field", "cont_input": "input field", "cont_output": "output field", "cont_hint": "hint field", "source": "source field", "tags": "debug;", "spj": false, "show_level": 1}
```