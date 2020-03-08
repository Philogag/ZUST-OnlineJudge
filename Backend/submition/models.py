from django.db import models
from enum import IntEnum

lang_choices = (
    ("c++", "C++"),
    ("c", "C"),
    ("java", "JAVA"),
    ("py2", "Python2"),
    ("py3", "Python3")
)

class STATUE(IntEnum):
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
    WAITING = -2

to_choices = lambda enum: tuple([(int(v), str(v).split(".")[1]) for v in enum])

class Submition(models.Model):
    pid = models.IntegerField() # 问题id
    ptitle = models.CharField(max_length = 50, default="")
    contestid = models.IntegerField(default=-1) # 比赛归属
    user = models.CharField(max_length=20) # 提交人

    timestamp = models.DateTimeField(auto_now_add=True)

    lang = models.CharField(max_length=10, choices=lang_choices)  # 提交语言
    code = models.CharField(max_length=1024 * 1024)

    statue = models.IntegerField(choices=to_choices(STATUE))
    judger = models.CharField(max_length=20, default="localhost")
    statue_detail = models.CharField(max_length=1024 * 1024, default="")
    judger_msg = models.CharField(max_length=100, default="")

    max_mem_use_kb = models.IntegerField(default=0)
    max_time_use_ms = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)