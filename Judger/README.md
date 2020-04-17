
# 配置文件

## conf.json

**完整配置文件**
```json
{
  "judger name": "默认为本机ip",
  "judge thread": 4,

  "backend host": "rabbitmq:8000",
  "judger keygen": "it is right",

  "queue host": "localhost",
  "queue port": 5672,
  "username": "OnlineJudge",
  "password": "OnlineJudge",
  "judge queue": "JudgeQueue",

  "vjudge enabled": true,
  "vjudge username": "xxx",
  "vjudge password": "xxx",
}
```

逐行解释:
### 通用配置
+ `judger name`: 测评机名称，默认为ip
+ `judge thread`: 测评机线程数，默认4
### 后端配置
+ `backend host`: 后端地址
+ `judger keygen`: 测评身份验证
### 队列配置
+ `queue host`: 消息队列地址
+ `queue port`: 消息队列端口
+ `username`、`password`: 消息队列连接账户
+ `judge queue`: 队列名称,
### vjudge配置
+ `vjudge enabled`: 是否启用vjudge,
+ `vjudge username`、`vjudge password`: vjudge账户

> Vjudge交题爬虫默认只启用了HDU，CodeForces
> 如需其他配置请自行修改 `Judger/lib/judge/vjudge/LanguageMap.py`

## 编译配置
详见 `language.json`

# 生成测评事件

每个测评事件为一个json字典字符串，格式如下

## 常量
##### judge_method：
+ LocalJudge： 0
+ Vjudge： 1

```json
{
  "id": 1, //submition id
  "lang": "c++", // or "c" or "java" or "py3"
  "judge_method": 0, 
  "code": "#include<iostream>\nusing namespace std;\nint main()\n{\n\tint a,b;\n\tcin >> a >> b;\n\tcout << a + b << endl;\n}", 
  "pid": 1, 
  "real_pid": "", // or like “HDU-1001”, disabled when localjudge
  "spj": false,       // disabled when vjudge
  "time_limit": 1000, // disabled when vjudge
  "mem_limit": 64     // disabled when vjudge
}
```

# 返回测评结果
采用HTTP POST返回结果至后端