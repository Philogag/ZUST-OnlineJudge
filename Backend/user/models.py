from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from enum import IntEnum
# Create your models here.

class USER_LEVEL(IntEnum):
    GUEST = -1
    USER = 0
    ADMIN = 1
    TEMP = 2

to_choices = lambda enum: tuple([(int(v), str(v).split(".")[1]) for v in enum])

class User(AbstractBaseUser):
    token = models.CharField(max_length=50)
    last_login = models.DateTimeField()
    
    ac_cnt = models.IntegerField(default=0)
    tot_cnt = models.IntegerField(default=0)

    school = models.CharField(max_length=50)
    sch_id = models.IntegerField(default=0)  # 学号
    
    user_level = models.IntegerField(default=0, choices=(to_choices(USER_LEVEL)))

